#!/usr/bin/env bash
# start-dev.sh - Start both API and Web servers locally
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC_DIR="$SCRIPT_DIR/src"
WEB_DIR="$SCRIPT_DIR/web-server"

echo "Starting API server (Flask on :5050)..."
cd "$SRC_DIR"
nohup venv/bin/gunicorn -w 2 -b 0.0.0.0:5050 api:app \
  --access-logfile /tmp/ode-api-access.log \
  --error-logfile /tmp/ode-api-error.log \
  --pid /tmp/ode-api.pid \
  > /dev/null 2>&1 &
echo "  API PID: $!"

echo "Starting Web server (Vite on :8024)..."
cd "$WEB_DIR"
nohup npx vite --host \
  > /tmp/ode-web.log 2>&1 &
echo "  Web PID: $!"

echo ""
echo "✅ Both servers started!"
echo "   Frontend: http://localhost:8024"
echo "   API:      http://localhost:5050"
echo ""
echo "To stop: kill \$(cat /tmp/ode-api.pid) && lsof -ti:8024 | xargs kill"
echo "Logs: tail -f /tmp/ode-api-*.log /tmp/ode-web.log"
