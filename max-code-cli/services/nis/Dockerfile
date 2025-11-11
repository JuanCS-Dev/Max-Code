FROM python:3.11-slim

WORKDIR /app

RUN pip install fastapi uvicorn

COPY app.py .

EXPOSE 8153

CMD ["python", "app.py"]
