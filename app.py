from flask import Flask, request, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create Gemini model
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Prometheus metrics
REQUEST_COUNT = Counter("api_requests_total", "Total API requests", ["endpoint"])

@app.route("/")
def home():
    REQUEST_COUNT.labels(endpoint="/").inc()
    return "✅ Weather DevOps App is running successfully!"

@app.route("/metrics")
def metrics():
    REQUEST_COUNT.labels(endpoint="/metrics").inc()
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

@app.route("/ask", methods=["POST"])
def ask_gemini():
    REQUEST_COUNT.labels(endpoint="/ask").inc()
    try:
        data = request.get_json()
        question = data.get("question")
        if not question:
            return jsonify({"error": "Missing 'question' field"}), 400
        response = model.generate_content(question)
        return jsonify({"answer": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)