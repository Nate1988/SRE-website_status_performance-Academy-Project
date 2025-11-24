from flask import Flask, render_template_string, Response
import threading
import requests
import time
import logging

from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST

# --- OpenTelemetry imports ---
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter  # ✅ FIXED
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# --- Tracing setup ---
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "website-checker"})
    )
)
tracer = trace.get_tracer(__name__)

# OTLP Exporter
otlp_exporter = OTLPSpanExporter(
    endpoint="otel-collector:4317",
    insecure=True,
)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

# --- Flask App Setup ---
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# --- Instrument Flask and Requests ---
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

# --- URLs to Monitor ---
URLS = [
    "https://www.youtube.com/",
    "https://www.facebook.com/?locale=es_LA",
    "https://www.instagram.com/",
    "https://x.com/?lang=es",
    "https://web.telegram.org/k/",
    "https://www.reddit.com/",
    "https://www.snapchat.com/",
    "https://ibm.com/lightning/page/home",
    "https://www.tiktok.com/es/",
]

# --- Prometheus Metrics ---
response_time_gauge = Gauge('website_response_time_seconds', 'Response time of websites', ['url'])
status_gauge = Gauge('website_up', 'Website up status (1=up, 0=down)', ['url'])

# --- Result Store for Flask UI ---
results = []

# --- HTML Template for Dashboard ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Website Status Checker</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        table { width: 80%; border-collapse: collapse; }
        th, td { padding: 10px; border: 1px solid #ccc; text-align: left; }
        th { background-color: #f2f2f2; }
        .up { color: green; }
        .down { color: red; }
    </style>
</head>
<body>
    <h2>Website Status & Performance (Auto-Refreshed)</h2>
    {% if results %}
    <table>
        <tr>
            <th>URL</th>
            <th>Status</th>
            <th>Response Time (s)</th>
        </tr>
        {% for result in results %}
        <tr>
            <td>{{ result['url'] }}</td>
            <td class="{{ 'up' if result['status'] == 'Up' else 'down' }}">{{ result['status'] }}</td>
            <td>{{ result['response_time'] }}</td>
        </tr>
        {% endfor %}
    </table>
    {% else %}
    <p>No websites to check.</p>
    {% endif %}
</body>
</html>
"""

# --- Website Checker Function ---
def check_websites():
    global results
    while True:
        logging.info("Performing periodic website checks...")
        current_results = []

        for url in URLS:
            with tracer.start_as_current_span("check_single_website") as span:
                span.set_attribute("url", url)
                try:
                    start = time.time()
                    response = requests.get(url, timeout=5)
                    elapsed = round(time.time() - start, 3)

                    if response.status_code == 200:
                        status = "Up"
                        status_gauge.labels(url=url).set(1)
                    else:
                        status = "Down"
                        status_gauge.labels(url=url).set(0)

                    response_time_gauge.labels(url=url).set(elapsed)

                except Exception as e:
                    logging.error(f"Error checking {url}: {e}")
                    elapsed = "-"
                    status = "Down"
                    status_gauge.labels(url=url).set(0)
                    response_time_gauge.labels(url=url).set(0)

                current_results.append({'url': url, 'status': status, 'response_time': elapsed})

        results = current_results
        time.sleep(60)  # check every 60 seconds

# --- Flask Routes ---
@app.route('/')
def dashboard():
    with tracer.start_as_current_span("dashboard_view"):
        return render_template_string(HTML_TEMPLATE, results=results)

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# --- Start Application ---
if __name__ == '__main__':
    threading.Thread(target=check_websites, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
