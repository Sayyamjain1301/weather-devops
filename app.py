from flask import Flask, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

# Initialize Flask app
app = Flask(__name__)

# Create Prometheus metric
REQUEST_COUNT = Counter(
    'weather_requests_created_total',
    'Total number of weather API requests handled'
)

@app.route('/')
def home():
    """Main route - increments the request counter."""
    REQUEST_COUNT.inc()
    return "✅ Weather DevOps App is running successfully!"

@app.route('/metrics')
def metrics():
    """Expose Prometheus metrics."""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    # Run Flask on all network interfaces so Prometheus can access it
    app.run(host="0.0.0.0", port=8080)