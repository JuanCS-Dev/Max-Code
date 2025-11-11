FROM python:3.11-slim

WORKDIR /app

RUN pip install fastapi uvicorn

COPY app.py .

EXPOSE 8152

CMD ["python", "app.py"]
