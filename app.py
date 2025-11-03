from flask import Flask, jsonify, request
from dotenv import load_dotenv
import google.generativeai as genai
import requests
import os
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

# ------------------ Load environment variables ------------------
load_dotenv()

app = Flask(__name__)

# ------------------ API Keys ------------------
GEMINI_KEY = os.getenv("GEMINI_KEY")
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")

# Check keys
if not GEMINI_KEY or not OPENWEATHER_KEY:
    raise ValueError("⚠️ Missing API keys! Check your .env file.")

# ------------------ Configure Gemini ------------------
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ------------------ Prometheus Metrics ------------------
REQUEST_COUNT = Counter("app_requests_total", "Total number of requests received")

# ------------------ Health Check ------------------
@app.route("/")
def home():
    return "✅ Weather DevOps App is running successfully!"

# ------------------ Weather API ------------------
@app.route("/weather", methods=["GET"])
def get_weather():
    REQUEST_COUNT.inc()

    city = request.args.get("city")
    if not city:
        return jsonify({"error": "Please provide a city name"}), 400

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"
    response = requests.get(weather_url)
    
    if response.status_code != 200:
        return jsonify({"error": "City not found"}), 404

    data = response.json()
    weather_desc = data["weather"][0]["description"]
    temp = data["main"]["temp"]

    result = {
        "city": city,
        "temperature": temp,
        "description": weather_desc
    }

    return jsonify(result)

# ------------------ AI Assistant ------------------
@app.route("/ask", methods=["POST"])
def ask_gemini():
    REQUEST_COUNT.inc()

    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "Please provide a question"}), 400

    try:
        response = model.generate_content(question)
        return jsonify({"answer": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------ Prometheus Metrics Endpoint ------------------
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

# ------------------ Run App ------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"🌍 Starting Weather + AI Assistant on port {port}...")
    app.run(host="0.0.0.0", port=port)