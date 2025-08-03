version: '3.8'
services:
  ai_service:
    build: .
    volumes:
      - ./timetracker.db:/app/timetracker.db
    ports:
      - "8000:8000"
  gui:
    image: python:3.10-slim
    volumes:
      - .:/app
      - ./timetracker.db:/app/timetracker.db
    working_dir: /app
    command: python app.py
    depends_on:
      - ai_service
    environment:
      - TIMETRACKER_DB_PATH=timetracker.db
    # to show GUI from container, you'd need X11 forwarding or run locally
