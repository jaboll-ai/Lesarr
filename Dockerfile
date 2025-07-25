FROM node:22-alpine AS build-env
WORKDIR /app/frontend
COPY frontend/ .
RUN npm install && npm run build

FROM mcr.microsoft.com/playwright/python:v1.54.0-noble
WORKDIR /app
COPY requirements.txt entry.py ./
COPY backend/ ./backend
COPY --from=build-env /app/frontend/dist ./frontend/dist
RUN  pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["python","entry.py"]

