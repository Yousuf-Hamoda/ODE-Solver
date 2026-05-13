# ---- API stage ----
FROM python:3.12-slim AS api
WORKDIR /app
COPY src/requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5050", "api:app"]

# ---- Web stage ----
FROM node:20-alpine AS web
WORKDIR /app
COPY web-server/package*.json .
RUN npm install
COPY web-server/ .
CMD ["npm", "run", "dev", "--", "--host"]