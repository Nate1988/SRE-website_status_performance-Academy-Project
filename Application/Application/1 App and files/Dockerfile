FROM python:3.11-slim

WORKDIR /app

COPY website_status_performance.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
EXPOSE 9300

CMD ["python", "website_status_performance.py"]
