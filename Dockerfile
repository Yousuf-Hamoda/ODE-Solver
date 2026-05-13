# ---- API stage ----
FROM python:3.12-slim AS api
WORKDIR /app
COPY src/requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .
CMD ["python", "api.py"]

# ---- Web stage ----
FROM node:20-alpine AS web
WORKDIR /app
COPY web-server/package*.json .
RUN npm install
COPY web-server/ .
CMD ["npm", "run", "dev", "--", "--host"]