# ---- API stage ----
FROM python:3.12-slim AS api
WORKDIR /app
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5050", "api:app"]

# ---- Web build stage ----
FROM node:20-alpine AS web-build
WORKDIR /app
COPY web-server/package*.json ./
RUN npm ci
COPY web-server/ .
RUN npm run build

# ---- Web runtime stage ----
FROM nginx:1.27-alpine AS web
COPY web-server/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=web-build /app/dist /usr/share/nginx/html
EXPOSE 8024
CMD ["nginx", "-g", "daemon off;"]
