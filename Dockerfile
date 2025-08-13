FROM python:3.11-slim

WORKDIR /app

COPY ./backend/requirements.txt ./backend/requirements.txt

RUN pip install --no-cache-dir -r ./backend/requirements.txt

COPY ./backend ./backend
COPY ./frontend ./frontend

EXPOSE 8080

CMD ["python3", "./backend/main.py"]
