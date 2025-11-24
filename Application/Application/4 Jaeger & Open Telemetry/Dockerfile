FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y build-essential curl && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY website_status_performance.py .

CMD ["python", "website_status_performance.py"]
