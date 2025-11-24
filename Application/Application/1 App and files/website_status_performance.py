from flask import Flask, render_template_string
import threading
import requests
import time
import logging
from prometheus_client import start_http_server, Gauge

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

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

# Prometheus metrics
response_time_gauge = Gauge('website_response_time_seconds', 'Response time of websites', ['url'])
status_gauge = Gauge('website_up', 'Website up status (1=up, 0=down)', ['url'])

# Store results for the Flask web view
results = []

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

def check_websites():
    global results
    while True:
        logging.info("Performing periodic website checks...")
        current_results = []

        for url in URLS:
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


@app.route('/')
def dashboard():
    return render_template_string(HTML_TEMPLATE, results=results)


if __name__ == '__main__':
    # Start Prometheus metrics HTTP server on port 9300
    start_http_server(9300, addr="0.0.0.0")

    # Start background thread for periodic checks
    threading.Thread(target=check_websites, daemon=True).start()

    # Start Flask app
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
