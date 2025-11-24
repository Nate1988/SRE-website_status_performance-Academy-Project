











# Website Status Performance App

This project implements a Python-based uptime monitoring application built with Flask and Requests. It integrates seamlessly with Prometheus for metric scraping and uses Grafana to visualize performance and availability metrics through custom dashboards. Additionally, the system includes Jaeger via OpenTelemetry to provide distributed tracing across application components, enabling deep visibility into request flows and performance bottlenecks.

The entire solution runs in a WSL Ubuntu Kubernetes environment, where Prometheus Alertmanager is configured to trigger real-time alerts in case of service outages, latency spikes, or other system failures. Grafana dashboards, Jaeger tracing views, and alerts together deliver a complete, observable monitoring stack.

## Table of Contents

- [Architecture](#architecture)  
- [Requirements](#requirements)  
- [Project Structure](#project-structure)  
- [Local Deployment](#local-deployment-step-by-step)
  *   [WSL Local Pyton Application Running](#1-wsl-local-pyton-application-running)
  *   [Full application Code](#Full-application-Code)
  *   [Running the app as a service Deployment Docker image usinging Kubernetes resources](#2-local-deployment-running-the-app-as-a-service-deployment-docker-image-usinging-kubernetes-resources
)
  * [The monitoring stack Prometheus, Grafana, Alertmanager and your applications Kubernetes resources](#3-deploy-the-monitoring-stack-prometheus-grafana-alertmanager-and-your-applications-kubernetes-resources)
- [Observability](#observability)  
- [Alerts](#alerts)  
- [Advanced Options](#advanced-options)  
- [License](LICENSE.md)  
- [Contributing](CONTRIBUTING.md)

---

## Architecture

-   **Python 3.13.6** Python, used to run and develop Python applications. It includes the core runtime and tools like pip for installing packages.
Required libraries (such as Flask, Requests, Prometheus client, OpenTelemetry SDK, etc.) are installed separately with pip to add features your app needs.
	 **WSL Ubunto**: Runs a lightweight Ubuntu Linux environment directly on Windows using Windows Subsystem for Linux (WSL).
Provides native Linux kernel compatibility for running Kubernetes, Docker, and related tools.
Enables seamless development and deployment of containerized apps within Windows without a VM.
-   **Flask App**: Built with Flask, it periodically checks URLs listed in urls.yaml.
Exposes /status for health and /metrics endpoint for Prometheus metrics.
Metrics include uptime and response latency per URL.
-   **Prometheus**: Scrapes Flask app’s /metrics every 10 seconds via ServiceMonitor.
Stores time-series data for URL availability and latency metrics.
Enables querying with PromQL for monitoring and alerting.
-   **Grafana**: Connects to Prometheus as data source for visualizing metrics.
Displays dashboards showing uptime, latency, and error trends.
Supports customizable panels for detailed URL monitoring.
-   **Alertmanager**: Receives alerts from Prometheus based on defined rules (e.g., URL down).
Handles alert routing, grouping, and silencing.
-   **Jeager Open Telemetry**: OpenTelemetry collects tracing data from your application in a standard, vendor-neutral way.
It sends those traces to Jaeger, which stores and visualizes them.
Together, they let you see end-to-end request flows and diagnose performance or reliability issues.
Sends notifications to Slack, email, or other receivers
-   **Kubernetes**: Manages containerized app stack via deployments and services.
Uses ConfigMaps for configs like urls.yaml and Prometheus scrape configs.
Handles orchestration, scaling, and self-healing of components.
-   **kubectl** Is the command-line tool used to interact with a Kubernetes cluster. It lets you deploy applications, check logs, inspect resources, and manage anything running inside Kubernetes.
In simple terms: kubectl is how you control Kubernetes.
- **Minikube** Is a tool that lets you run a lightweight, single-node Kubernetes cluster on your own computer.
It’s mainly used for learning, development, and testing Kubernetes locally. In simple terms: Minikube gives you a personal Kubernetes cluster on your laptop.
- **Docker** Is a platform that packages applications into containers, which are lightweight, portable, and run the same everywhere.
It ensures your app and all its dependencies run consistently across machines. In simple terms: Docker lets you build once and run anywhere.
- **Podman** is a container engine similar to Docker but designed to run containers without needing a background daemon.
It supports rootless containers, making it more secure by default.
In simple terms: Podman runs containers like Docker, but without the daemon and with stronger security.
- **Docker File** A Dockerfile is a text file that contains step-by-step instructions for building a Docker image.
It tells Docker what base image to use, what files to copy, which commands to run, and how to start the app.
In simple terms: a Dockerfile is the recipe Docker uses to bake your container.
- **YAML File** A YAML file is a simple, human-readable text format used to store configuration data.
It uses indentation (spaces) to show structure instead of brackets or symbols.
In simple terms: YAML is an easy way to write settings for tools like Docker Compose, Kubernetes, and CI/CD systems.

---

## Requirements

-   WSL2 and Ubuntu
-   Python python-3.13.6-amd64.exe and requiere Liberies
-   Docker
-   Docker and Yaml files  
-   Minikube 
-   kubectl  
-   Prometheus
-   Grafana
-   Jeager Open Telemetry

---

## Project Structure

```


├── Application
│   ├─── App & files  
│   |      ├── Dockerfile
|   |      ├── requirements.txt
|   |      └── website_status_performance.py
|   |      
|   ├─── Scraping Prometheus files    
│   |      ├── prometheus.yaml
|   |      ├── metrics.txt
|   |      └── Prometheus Scraping.png
|   |
|   ├─── Monitoring Grafana Files & Dashboards Review
|   |     └── grafana.yaml
|   |
│   ├─── Jaeger & Open Telemetry
│   |      ├── docker-compose.yaml
|   |      ├── Dockerfile
│   |      ├── otel-collector-config.yaml
|   |      ├── alertmanager-deployment.yaml
|   |      ├── requirements.txt
|   |      └── website_status_performance.py
│   |
│   ├─── Alert Manager files
│   |      ├── alertmanager-config.yaml
|   |      ├── alertmanager-deployment.yaml
|   |      ├── prometheus.yaml
|   |      └── prometheus-alert-rules.yaml
│   ├─── Evidence
│   |      ├── 1.1 Website Performance expected behaviour.png
|   |      ├── 1.2 Docker website status performance.pngl
|   |      ├── 1.3 Public repository website_status_performance_1.1.png
|   |      ├── 1.4 Minikube website status performance deploment.png
|   |      ├── 1.5 Prometheus is Scraping Metrics.png
|   |      ├── 1.6 Grafana is vizualizing Metrics.png
|   |      └── 1.7 Grafana is vizualizing Dashboards.png
|   |
│   ├─── Docker Compose files (optional)
│   |      ├── grafana /dashboards and /datasources
|   |      ├── docker-composeJaeger-Prometheus.yaml
|   |      ├── otel-collector-config.yaml
|   |      ├── prometheus.yml
|   |      ├── requirements.txt
|   |      └── website_status_performance.py
|   |
├── CONTRIBUTING.md
├── LICENSE.md
└── README.md

````

---

## Local Deployment Step by Step

 ## 1 WSL Local Pyton Application Running

1.1)  **WSL 2 and Ubunto (Windows Subsystem for Linux)**:
   
  *Open PowerShell as Administrator.*
     
```bash
   wsl --install
```
  *Restart your computer when prompted.*
    
  *After reboot, Open Ubuntu command line to set up your Linux user (username & password).*

1.2) **Install Python 3.13.6 and required libraries flask & requests**:
```bash
   sudo apt update && sudo apt install -y wget build-essential libssl-dev zlib1g-dev libffi-dev python3-pip
   wget https://www.python.org/ftp/python/3.13.6/Python-3.13.6.tgz
   tar -xvf Python-3.13.6.tgz && cd Python-3.13.6 && ./configure --enable-optimizations && make -j$(nproc) && sudo make altinstall
   python3.13 -m pip install --upgrade pip
   python3.13 -m pip install flask requests
```

1.3) **Created the python application**:
   
   *This application is designed to monitor a predefined set of websites, with the target URLs configured directly in the application code. It checks whether each website is up or down and measures its response time, providing basic uptime and performance monitoring.*

   *To be able to run thbis application we need tro me sure that that below Libraries are installed: Flash and Request*
   *This was already completed on step 2*

```bash
   python -m pip install flask
   python -m pip install requests
```
---   
   ## Full application Code

      
```bash
   # Import required libraries
from flask import Flask, render_template_string  # Flask for web server and inline HTML rendering
import threading                                 # For running background tasks
import requests                                  # To make HTTP requests to websites
import time                                      # To measure response time and handle sleep
import logging                                   # For logging status and errors
from prometheus_client import start_http_server, Gauge  # Prometheus client for metrics collection

# Initialize the Flask web app
app = Flask(__name__)

# Set up basic logging to display INFO and higher-level logs
logging.basicConfig(level=logging.INFO)

# List of websites to monitor
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

# Prometheus metric: response time for each website (labeled by URL)
response_time_gauge = Gauge(
    'website_response_time_seconds',
    'Response time of websites',
    ['url']
)

# Prometheus metric: 1 if website is up, 0 if down (labeled by URL)
status_gauge = Gauge(
    'website_up',
    'Website up status (1=up, 0=down)',
    ['url']
)

# This list will store the latest check results to be shown in the web UI
results = []

# HTML template used to render the status dashboard
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

# Background function that checks all websites every 60 seconds
def check_websites():
    global results  # Needed to update the global `results` list

    while True:
        logging.info("Performing periodic website checks...")
        current_results = []  # Temporarily store this round of checks

        for url in URLS:
            try:
                # Record start time
                start = time.time()
                # Make a GET request with a 5-second timeout
                response = requests.get(url, timeout=5)
                # Calculate elapsed time
                elapsed = round(time.time() - start, 3)

                # Check if the site is up (status code 200)
                if response.status_code == 200:
                    status = "Up"
                    status_gauge.labels(url=url).set(1)  # Prometheus: site is up
                else:
                    status = "Down"
                    status_gauge.labels(url=url).set(0)  # Prometheus: site is down

                # Set response time in Prometheus
                response_time_gauge.labels(url=url).set(elapsed)

            except Exception as e:
                # If any error occurs (timeout, DNS, etc.), log it and mark as down
                logging.error(f"Error checking {url}: {e}")
                elapsed = "-"  # Display dash for response time
                status = "Down"
                status_gauge.labels(url=url).set(0)
                response_time_gauge.labels(url=url).set(0)

            # Store the result for the UI
            current_results.append({
                'url': url,
                'status': status,
                'response_time': elapsed
            })

        # Update the global results with the latest check
        results = current_results

        # Wait for 60 seconds before next round
        time.sleep(60)


# Flask route to display the HTML dashboard
@app.route('/')
def dashboard():
    # Render the HTML template and pass the current `results` list
    return render_template_string(HTML_TEMPLATE, results=results)


# Main entry point
if __name__ == '__main__':
    # Start Prometheus metrics server on port 9300 (accessible at /metrics)
    start_http_server(9300, addr="0.0.0.0")

    # Start the website checker in a separate background thread
    threading.Thread(target=check_websites, daemon=True).start()

    # Start the Flask web server on port 5000
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

      
```
---

1.4)    **Run the application**: 

*We need to go to the Application path, then run the below commands:*

  My application location path:\Academy\Github repository\SRE-website_status_performance\Applications\1 App and files

```bash
   python3 website_status_performance.py
```
  Or       
```bash
  python -m venv venv
  venv\Scripts\activate
  python.py
```

  Note: This picture 1.1 located in evidence folder will show the Website Performance expected behaviour.  

----

## 2 Local Deployment Running the app as a service Deployment Docker image usinging Kubernetes resources



2.1)  **Running the app as a service Deployment Docker image usinging Kubernetes**:

    **Deployment prerequisites**
 
2.2)  **Install docker**:Installed docker Destop https://www.docker.com/products/docker-desktop
          docker desktop version (optional)
```bash
  sudo apt update && sudo apt upgrade -y
  sudo apt install -y docker.io
  sudo systemctl enable docker
  sudo systemctl start docker     
```
2.3)  **Install Minikube**:
```bash
  sudo apt install -y curl apt-transport-https
  curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
  sudo install minikube-linux-amd64 /usr/local/bin/minikube
```
2.4)  **Install kubectl**:
```bash
  sudo apt install -y kubectl
```
2.5)  **Review Prerequisites installation**:
```bash
  docker --version
  minikube version
  kubectl version --client  
```
  **Deployment Configuration Docker and requirements file**
    
2.6)  **Docker File**:
```bash
  FROM python:3.11-slim

  WORKDIR /app

  # Copy your Python script and requirements
  COPY website_status_performance.py /app/
  COPY requirements.txt /app/

  # Install dependencies
  RUN pip install --no-cache-dir -r requirements.txt

  EXPOSE 5000

  CMD ["python", "website_status_performance.py"]

```
  This docker File its a file without any extension. and needs to  be place in the same application folder
    
2.7)  **Requirements file**:
```bash
   blinker==1.9.0
   certifi==2025.7.14
   charset-normalizer==3.4.2
   click==8.2.1
   colorama==0.4.6
   Flask==3.1.1
   idna==3.10
   itsdangerous==2.2.0
   Jinja2==3.1.6
   MarkupSafe==3.0.2
   requests==2.32.4
   urllib3==2.5.0
   Werkzeug==3.1.3
```
  Note 1: I add  --no-cache-dir -r requirements.txt in the dockfile

  Note 2: run pip freeze > requirements.txt in the directory to  collected the application  requirements to avoid any No module named error when creating the Docker image

  Note 3: This file needs to be place in the same application folder
    
2.8)  **Building the Container Image with Docker:** 

We need to go to the Application path, then run the below commands:

  My application location path:\Academy\Github repository\SRE-website_status_performance\Applications\1 App and files

  To Create the Image
```bash
  docker build -t website-status-performance .
```
  To Run and test the created image       
     
```bash
  docker run --rm -it -p 5000:5000 website-status-performance 
```
  Note: This picture 1.2 located in Evidence folder will show the Website Performance expected behaviour.
    
2.9) **Created Docker Hub account**:
   
 * Visit Docker Hub: Navigate to [Docker Hub.](https://hub.docker.com/)

 * Create the public repository my case website_status_performance_1.1 Using this description(This application review website's performance by reviewing if it's up or down and the response time)
	
 Note: This picture 1.3 located in the evidence folder will show the Public Repository that was created in Docker. 
   
2.10) **Tag the Local Image**:
   
  *Tags a local Docker image with a new name (nates1988/website_status_performance_1.1:latest) for uploading to a remote registry like Docker Hub.*
	
```bash
  docker tag website-status-performance:latest nates1988/website_status_performance_1.1:latest
```
  *Uploads the tagged Docker image nates1988/website_status_performance_1.1:latest to Docker Hub.*
  
```bash
  docker push nates1988/website_status_performance_1.1:latest
```
  *Runs the Docker image nates1988/website_status_performance_1.1:latest interactively, maps port 5000 to host, and removes the container after it exits.*
  
```bash
  docker run --rm -it -p 5000:5000 nates1988/website_status_performance_1.1:latest
```
  Note 1 Navigate to the Repositories section on the left sidebar in  Docker Hub https://hub.docker.com/repositories/nates1988 and we will be able to see the Repository
  Note:2  This picture 1.4 located in the evidence folder will show the Public Repository that was created in Docker. 
    
2.11) **Configure Minikube to Use Docker**: *We need to go to the Application path, then run the below commands:*

  My application location path:\Academy\Github repository\SRE-website_status_performance\Applications
   
  *This command points your local `docker` CLI to Minikube's internal Docker , allowing you to build images directly into the Minikube VM.*
```bash
  eval $(minikube docker-env)  / eval $(minikube docker-env -u)
```
  *Run Minikube*
```bash
  minikube start --driver=docker
```

2.12) **Create the deployment.yaml and service.yaml**:
  
  *deployment.yaml  my file*
```bash
         apiVersion: apps/v1
         kind: Deployment
         metadata:
           name: website-checker-deployment
         spec:
           replicas: 1
           selector:
             matchLabels:
               app: website-checker
           template:
             metadata:
               labels:
                 app: website-checker
             spec:
               containers:
               - name: website-checker
                 image: website-status-performance
                 imagePullPolicy: Never
                 ports:
                 - containerPort: 5000

```
  *service.yaml my file*

```bash
         apiVersion: v1
         kind: Service
         metadata:
           name: website-checker-service
         spec:
         type: NodePort
         selector:
             app: website-checker
         ports:
         - port: 80          # External port users will connect to
         targetPort: 5000  # Internal Flask app port inside the container


```
2.13) **Deployed and test deployment.yaml & service.yaml**:

  *Deployed the Deployment and service yamal files*
   
```bash
          kubectl apply -f website-checker-deployment.yaml
          kubectl apply -f website-checker-Service.yaml 
```
  *Run  the Deployment*
	
```bash
         minikube dashboard
         minikube service website-checker-service     
```
  Note: This picture 1.5 in the evidence folder will show Load Image into Minikube (Deploying the Application)

---
   ## 3 Deploying and reviewing traces, Metrics and Alerts in Prometheus, Grafana, Jeager Open Telemetry and Alertmanager for an application and Kubernetes resources.
   
*We need to go to the Application path, then run the below commands:*

  My application location path:\Academy\Github repository\SRE-website_status_performance\Applications\2 Prometheus files
		 
  3.1) **Prometheus Inatallation:**		 
	 
```bash
   sudo apt update
   sudo apt install prometheus
```
*Wait for the Prometheus Installation.*
     
  *Start Prometheus*
	 
```bash
   sudo systemctl start prometheus
   sudo systemctl enable prometheus
```
    
 3.2  **Prometheus configuration:** 
 
  *Namespace Creation: We isolate monitoring components in their own namespace*
	 
```bash
   kubectl create namespace monitoring
```
3.3)  **Create Prometheus Configuration manifest file in one:( it will contained :configmap,Deployment and service)**

```bash
    apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: website
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s

    scrape_configs:
      - job_name: 'website-monitor'
        static_configs:
          - targets: ['website-monitor-service:9300']

      - job_name: 'cadvisor'
        kubernetes_sd_configs:
          - role: pod
            namespaces:
              names:
                - default
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_label_app]
            action: keep
            regex: cadvisor
        metrics_path: /metrics
        scheme: http

```
  3.4) **Apply the Prometheus manifest file**

```bash
   kubectl apply -f prometheus.yam
```
 3.5) **Access the Prometheus**

```bash
    minikube service prometheus-service -n monitoring
    minikube service start prometheus-service -n website
```
 Or

```bash
      kubectl port-forward svc/prometheus-service -n website 9091:9090
```
 
Note: This picture 1.5 in the evidence folder will show how Prometheus is Scraping Metrics

 3.6) **Grafana Installation**

 *We need to go to the Application path, then run the below commands:*

  My application location path:\Academy\Github repository\SRE-website_status_performance\Applications\3 Grafana Files

```bash
   sudo apt update && \
   sudo apt install -y apt-transport-https software-properties-common wget gnupg && \
   sudo wget -q -O - https://packages.grafana.com/gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/grafana.gpg && \
   echo "deb [signed-by=/usr/share/keyrings/grafana.gpg] https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list > /dev/null && \
   sudo apt update && \
   sudo apt install -y grafana

```
Start Grafana

```bash
   sudo systemctl start grafana-server
   sudo systemctl enable grafana-serve
```
3.3)  **Create Grafana Configuration manifest file in one:( it will contained :Deployment, Configuring Prometheus as a Data Source and Provisioning Dashboards)**

```bash
   # 1. Dashboard ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboards-config
  namespace: website
  labels:
    app: grafana
    grafana_dashboard: "1"
data:
  dashboards.yaml: |
    apiVersion: 1
    providers:
      - name: 'default'
        orgId: 1
        folder: ''
        type: file
        disableDeletion: false
        options:
          path: /etc/grafana/provisioning/dashboards
  example-dashboard.json: |
    {
      "id": null,
      "uid": "example-dashboard",
      "title": "Website + System Metrics",
      "tags": [],
      "style": "dark",
      "timezone": "browser",
      "editable": true,
      "schemaVersion": 36,
      "version": 1,
      "panels": [
        {
          "id": 1,
          "title": "Website Monitor Status (up)",
          "type": "timeseries",
          "datasource": "Prometheus",
          "gridPos": { "h": 6, "w": 24, "x": 0, "y": 0 },
          "targets": [
            {
              "expr": "up{job=\"website-monitor\"}",
              "refId": "A"
            }
          ]
        },
        {
          "id": 2,
          "title": "Website Availability (website_up)",
          "type": "timeseries",
          "datasource": "Prometheus",
          "gridPos": { "h": 6, "w": 24, "x": 0, "y": 6 },
          "targets": [
            {
              "expr": "website_up",
              "refId": "A"
            }
          ]
        },
        {
          "id": 3,
          "title": "Website Response Time (website_response_time_seconds)",
          "type": "timeseries",
          "datasource": "Prometheus",
          "gridPos": { "h": 6, "w": 24, "x": 0, "y": 12 },
          "targets": [
            {
              "expr": "website_response_time_seconds",
              "refId": "A"
            }
          ]
        },
        {
          "id": 4,
          "title": "Pod CPU Usage (cAdvisor)",
          "type": "timeseries",
          "datasource": "Prometheus",
          "gridPos": { "h": 6, "w": 24, "x": 0, "y": 18 },
          "targets": [
            {
              "expr": "sum(rate(container_cpu_usage_seconds_total[5m])) by (container_label_io_kubernetes_pod_name)",
              "refId": "A"
            }
          ]
        }
      ]
    }

---

# 2. Datasource ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-datasources
  namespace: website
  labels:
    app: grafana
    grafana_datasource: "1"
data:
  prometheus-datasource.yaml: |
    apiVersion: 1
    datasources:
      - name: Prometheus
        type: prometheus
        access: proxy
        url: http://prometheus-service:9090
        isDefault: true

---

# 3. Grafana Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
  namespace: website
  labels:
    app: grafana
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grafana
  template:
    metadata:
      labels:
        app: grafana
    spec:
      containers:
        - name: grafana
          image: grafana/grafana:latest
          ports:
            - containerPort: 3000
          env:
            - name: GF_SECURITY_ADMIN_USER
              value: admin
            - name: GF_SECURITY_ADMIN_PASSWORD
              value: admin
          volumeMounts:
            - name: grafana-storage
              mountPath: /var/lib/grafana
            - name: datasource-config
              mountPath: /etc/grafana/provisioning/datasources
            - name: dashboard-config
              mountPath: /etc/grafana/provisioning/dashboards
            - name: dashboards
              mountPath: /etc/grafana/provisioning/dashboards/dashboards
      volumes:
        - name: grafana-storage
          emptyDir: {}
        - name: datasource-config
          configMap:
            name: grafana-datasources
        - name: dashboard-config
          configMap:
            name: grafana-dashboards-config
            items:
              - key: dashboards.yaml
                path: dashboards.yaml
        - name: dashboards
          configMap:
            name: grafana-dashboards-config
            items:
              - key: example-dashboard.json
                path: example-dashboard.json

---

# 4. Grafana Service
apiVersion: v1
kind: Service
metadata:
  name: grafana-service
  namespace: website
spec:
  selector:
    app: grafana
  ports:
    - protocol: TCP
      port: 3000
      targetPort: 3000
  type: ClusterIP


```
  3.4) **Apply the Grafana manifest file**

```bash
   kubectl apply -f grafana.yaml
```
 3.5) **Access the Grafana**

```bash
   kubectl port-forward svc/grafana-service -n website 3001:3000
   http://localhost:3001
```
Note: This picture 1.6 in the evidence folder will show how Grafana is vizualizing Metrics

 3.5) **Open Telemetry and Jaeger** 

  *We need to go to the Application path, then run the below commands:*

  My application location path:\Academy\Github repository\SRE-website_status_performance\Applications\4 Jaeger & Open Telemetry

 
Create this  file docker-compose.yaml
```bash
   version: "3.9"

services:
  jaeger:
    image: jaegertracing/all-in-one:1.49
    ports:
      - "16686:16686"    # Jaeger UI
      - "14250:14250"    # Jaeger gRPC Collector (OTLP)
    environment:
      COLLECTOR_OTLP_ENABLED: "true"
      COLLECTOR_OTLP_GRPC_PORT: "14250"
    restart: unless-stopped

  otel-collector:
    image: otel/opentelemetry-collector:0.73.0
    volumes:
      - ./otel-collector-config.yaml:/etc/otel-collector-config.yaml
    command: ["--config", "/etc/otel-collector-config.yaml"]
    ports:
      - "4317:4317"    # OTLP gRPC receiver (app -> collector)
      - "8888:8888"    # Prometheus metrics scraping (optional)
    depends_on:
      - jaeger
    restart: unless-stopped

  website-status-app:
    build: .
    ports:
      - "5000:5000"
    environment:
      OTEL_EXPORTER_OTLP_ENDPOINT: "http://otel-collector:4317"
    depends_on:
      - otel-collector
    restart: unless-stopped

```
Create this  file Dockerfile
```bash
   FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y build-essential curl && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY website_status_performance.py .

CMD ["python", "website_status_performance.py"]

```
Create this  file otel-collector-config.yaml
```bash
   receivers:
  otlp:
    protocols:
      grpc:
      http:

exporters:
  jaeger:
    endpoint: "jaeger:14250"
    tls:
      insecure: true

service:
  telemetry:
    metrics:
      address: ":8889"   #  Changed to avoid conflict with existing service
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [jaeger]

```
Create this  file requirements.txt
```bash
   flask
requests
prometheus_client

# OpenTelemetry core + exporters + instrumentation (keep all at 1.22.0)
opentelemetry-api==1.22.0
opentelemetry-sdk==1.22.0
opentelemetry-exporter-otlp-proto-grpc==1.22.0

# Instrumentation
opentelemetry-instrumentation==0.43b0
opentelemetry-instrumentation-flask==0.43b0
opentelemetry-instrumentation-requests==0.43b0

```
Docker compuse (Optional)

  *We need to go to the Application path, then run the below commands:*

  My application location path:\Academy\Github repository\SRE-website_status_performance\Applications\7 Docker Compose files

**This are the instructions of using Docker compuse (optional) to be able to exicute and run we need to run the below commnad**

Docker Compose is a tool that lets you define and run multiple Docker containers using a single file (usually docker-compose.yml).

Exicute
```bash
   sudo apt update
   sudo apt install docker-compose
   docker-compose up --build
```
Run
```bash
   docker compose up
```
then

```bash
   App: http://localhost:5000
   Metrics: http://localhost:5000/metrics
   Jaeger UI: http://localhost:16686
```

Note 1 :This picture 1.7 in the evidence folder will show how traces were generated
Note 2: This picture 1.6 in the evidence folder will show how Grafana is vizualizing Metrics
For reference I have added all docker compose files on this location path:\Academy\Github repository\SRE-website_status_performance\Applications\7 Docker Compose files

 3.5) **Access the Grafana**

```bash
   kubectl port-forward svc/grafana-service -n website 3001:3000
   http://localhost:3001
```
Note: This picture 1.6 in the evidence folder will show how Grafana is vizualizing Metrics

 3.5) **Alert Manager**
 
   *We need to go to the Application path, then run the below commands:*

My application location path:\Academy\Github repository\SRE-website_status_performance\Applications\5 Alert Manager files

We need to apply the below code: alertmanager-config.yaml

```bash
   apiVersion: v1
  kind: ConfigMap
  metadata:
   name: alertmanager-config
   namespace: website
data:
  alertmanager.yml: |
    global:
      resolve_timeout: 5m

    route:
      receiver: 'slack-notifications'
      group_wait: 10s
      group_interval: 30s
      repeat_interval: 1h

    receivers:
      - name: 'slack-notifications'
        slack_configs:
          - api_url: 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX'
            channel: '#alerts'
            send_resolved: true
            title: '{{ .CommonLabels.alertname }}'
            text: '{{ range .Alerts }}{{ .Annotations.summary }}\n{{ end }}'

```
We need to apply the below code: alertmanager-deployment.yaml

```bash
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: alertmanager
     namespace: website
  spec:
  replicas: 1
  selector:
    matchLabels:
      app: alertmanager
  template:
    metadata:
      labels:
        app: alertmanager
    spec:
      containers:
        - name: alertmanager
          image: prom/alertmanager:v0.26.0
          args:
            - "--config.file=/etc/alertmanager/alertmanager.yml"
          ports:
            - containerPort: 9093
          volumeMounts:
            - name: config-volume
              mountPath: /etc/alertmanager
      volumes:
        - name: config-volume
          configMap:
            name: alertmanager-config
---
apiVersion: v1
kind: Service
metadata:
  name: alertmanager-service
  namespace: website
spec:
  selector:
    app: alertmanager
  ports:
    - protocol: TCP
      port: 9093
      targetPort: 9093
  type: ClusterIP

```
---
---

4.  **Port-forward services for local access**:

   *Port-forward services*  

   * **Uptime Monitor App (Metrics & Status):**
```bash
   POD_NAME=$(kubectl get pods -l app=website-checker -o jsonpath='{.items[0].metadata.name}')
   kubectl port-forward $POD_NAME 8000:5000 &

```
  * **Prometheus UI:**
```bash
   kubectl port-forward svc/prometheus-service -n website 9091:9090
```
* **Grafana UI:**
```bash
   kubectl port-forward svc/jaeger-service -n website 16686:16686
```
* **Jeager & Open Telemetry:**
  
```bash
   kubectl port-forward svc/grafana-service -n website 3001:3000
```
* **Alertmanager UI:**
  ```bash
     kubectl port-forward svc/grafana-service -n website 3001:3000 (Grafana)
     kubectl port-forward svc/alertmanager -n monitoring 9093:9093 (Alert Manager)
  ```

  
*URLs once port-forwarded*

* **Uptime Monitor App:**
   * App Status (JSON): `http://localhost:5000/`
   * Prometheus Metrics: `http://localhost:9300/metrics`
* **Prometheus UI:** `http://localhost:9091/targets`
* **Jeager Open telemetry UI:** `http://localhost:16686`
* **Grafana:** `http://localhost:3001`
* **Alertmanager UI:** `http://localhost:3001 or http://localhost:9093`

---

## Observability

To review the monitoring dashboard in Grafana, start by accessing the Grafana UI at http://localhost:3000. Log in using the default credentials (admin / admin), unless they have been changed. From the main menu, navigate to Dashboards and select Website + System Metrics.

Once you're viewing the dashboard, adjust the time range in the top-right corner to "Last 5 minutes" or "Last 15 minutes" to ensure you're seeing the most recent data—this is especially important if metric collection has only recently started. The dashboard provides key insights into service uptime, including:

* URL latency trends

* Website availability (Up/Down status)

* Response times
* Alerts been set to Slack

These visualizations help you monitor the availability and responsiveness of your web application in near real time.

Note: This picture 1.7 located in the evidence folder will show the Dashboars that were integrated in the Grafana file to have better Observability of these metrics. 

---

## Alerts

* Defined in `k8s/uptime-alert-rules.yaml`:
    * Trigger: `increase(uptime_check_failure_total[1m]) > 0`
* Alertmanager configuration (e.g., Slack webhook) can be added via Kubernetes Secret.
* **To test alerts manually:**
    * Ensure Alertmanager is port-forwarded (`http://localhost:9093`).
    * Run the following `curl` command (all on one line) to send a test alert. This alert will automatically expire after 5 minutes due to `endsAt`.
        ```bash
        curl -X POST -H "Content-Type: application/json" --data '[ { "labels": { "alertname": "ManualTestAlert", "severity": "critical", "instance": "manual-alert-source", "job": "test-job" }, "annotations": { "summary": "This is a manually generated test alert.", "description": "This alert was generated to test Alertmanager\'s functionality." }, "generatorURL": "[http://example.com/manual-alert](http://example.com/manual-alert)", "startsAt": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")", "endsAt": "$(date -u -d "+5 minutes" +"%Y-%m-%dT%H:%M:%SZ")" } ]' http://localhost:9093/api/v2/alerts
        ```
    * Verify the alert appears in the Alertmanager UI at `http://localhost:9093`.

---

## Advanced Options

This project is flexible and modular — you're free to customize and swap components based on your preferences or environment:

* Kubernetes Platforms: Minikube, Kind, GKE, EKS, AKS, IBM Cloud

* Application Stack: Flask, FastAPI, Node.js, Go, Ruby

* Infrastructure as Code (IaC): Terraform, Pulumi, Ansible

* Alerting Integrations: Slack, Email, Discord, PagerDuty

* CI/CD Pipelines: GitHub Actions, Jenkins, GitLab CI, ArgoCD

---

## Notes

-   This repository is part of a practical training series developed for the SRE Academy.
-   It is optimized for environments like Minikube but can be adapted to other Kubernetes setups.
-   Contributions and improvements are welcome. If you encounter issues or have suggestions, please open a pull request or GitHub issue.

Happy learning and implementing SRE best practices!

![Observability](https://img.shields.io/badge/Observability-Grafana%20%7C%20Prometheus-orange)
![Kubernetes](https://img.shields.io/badge/Platform-Kubernetes-informational)

---
