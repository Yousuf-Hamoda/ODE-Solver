#!/usr/bin/env bash
# start-dev.sh - Start both API and Web servers locally.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC_DIR="$SCRIPT_DIR/src"
WEB_DIR="$SCRIPT_DIR/web-server"
API_PORT="${API_PORT:-5050}"
WEB_PORT="${WEB_PORT:-8024}"
WEB_HOST="${WEB_HOST:-0.0.0.0}"
RUN_DIR="${RUN_DIR:-/tmp}"
API_PID_FILE="$RUN_DIR/ode-api.pid"
WEB_PID_FILE="$RUN_DIR/ode-web.pid"
API_ACCESS_LOG="$RUN_DIR/ode-api-access.log"
API_ERROR_LOG="$RUN_DIR/ode-api-error.log"
WEB_LOG="$RUN_DIR/ode-web.log"

port_is_in_use() {
  ss -ltn "( sport = :$1 )" | tail -n +2 | grep -q .
}

wait_for_port() {
  local pid="$1"
  local port="$2"

  for _ in $(seq 1 50); do
    if port_is_in_use "$port"; then
      return 0
    fi
    if ! kill -0 "$pid" 2>/dev/null; then
      return 1
    fi
    sleep 0.1
  done
  return 1
}

stop_started_api() {
  if [[ -n "${API_PID:-}" ]] && kill -0 "$API_PID" 2>/dev/null; then
    kill "$API_PID" 2>/dev/null || true
    wait "$API_PID" 2>/dev/null || true
  fi
  rm -f "$API_PID_FILE"
}

if port_is_in_use "$API_PORT"; then
  echo "API port $API_PORT is already in use; stop the existing service first." >&2
  exit 1
fi

if port_is_in_use "$WEB_PORT"; then
  echo "Web port $WEB_PORT is already in use; stop the existing service first." >&2
  exit 1
fi

if [[ -x "$SRC_DIR/venv/bin/gunicorn" ]]; then
  GUNICORN="$SRC_DIR/venv/bin/gunicorn"
elif [[ -x "$SCRIPT_DIR/.venv/bin/gunicorn" ]]; then
  GUNICORN="$SCRIPT_DIR/.venv/bin/gunicorn"
else
  echo "Gunicorn is not installed. Create a virtual environment and install src/requirements.txt." >&2
  exit 1
fi

if ! command -v npx >/dev/null 2>&1; then
  echo "npx is not installed; install Node.js and run npm install in web-server/." >&2
  exit 1
fi

mkdir -p "$RUN_DIR"
: > "$API_ACCESS_LOG"
: > "$API_ERROR_LOG"
: > "$WEB_LOG"

echo "Starting API server (Gunicorn on :$API_PORT)..."
(
  cd "$SRC_DIR"
  exec "$GUNICORN" -w 2 -b "0.0.0.0:$API_PORT" api:app \
    --access-logfile "$API_ACCESS_LOG" \
    --error-logfile "$API_ERROR_LOG"
) > /dev/null 2>&1 &
API_PID=$!

if ! wait_for_port "$API_PID" "$API_PORT"; then
  echo "API server failed to start. See $API_ERROR_LOG" >&2
  stop_started_api
  exit 1
fi
printf '%s\n' "$API_PID" > "$API_PID_FILE"
echo "  API PID: $API_PID"

echo "Starting Web server (Vite on :$WEB_PORT)..."
(
  cd "$WEB_DIR"
  exec npx vite --host "$WEB_HOST" --port "$WEB_PORT"
) > "$WEB_LOG" 2>&1 &
WEB_PID=$!

if ! wait_for_port "$WEB_PID" "$WEB_PORT"; then
  echo "Web server failed to start. See $WEB_LOG" >&2
  if kill -0 "$WEB_PID" 2>/dev/null; then
    kill "$WEB_PID" 2>/dev/null || true
  fi
  stop_started_api
  exit 1
fi
printf '%s\n' "$WEB_PID" > "$WEB_PID_FILE"
echo "  Web PID: $WEB_PID"

echo
echo "Both servers started."
echo "  Frontend: http://localhost:$WEB_PORT"
echo "  API:      http://localhost:$API_PORT"
echo
echo "To stop: kill \$(cat $API_PID_FILE) \$(cat $WEB_PID_FILE)"
echo "Logs: tail -f $API_ACCESS_LOG $API_ERROR_LOG $WEB_LOG"
