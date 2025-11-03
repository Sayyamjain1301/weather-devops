from flask import Flask, jsonify, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('weather_app_requests_total', 'Total number of requests')
REQUEST_LATENCY = Histogram('weather_app_request_latency_seconds', 'Request latency in seconds')

@app.route('/')
def home():
    REQUEST_COUNT.inc()
    return jsonify({"message": "Welcome to Weather DevOps App!"})

@app.route('/metrics')
def metrics():
    data = generate_latest()
    return Response(data, mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)