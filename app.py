from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

app = Flask(__name__)

# -----------------------------
# Prometheus Metrics
# -----------------------------
weather_requests_total = Counter(
    'weather_app_requests_total',
    'Total number of requests handled by the weather app'
)

# -----------------------------
# API Keys
# -----------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# -----------------------------
# Routes
# -----------------------------

@app.route('/')
def home():
    return jsonify({
        "message": "🌦️ Weather + AI Assistant is running successfully!",
        "endpoints": ["/weather?city=CityName", "/metrics"]
    })

@app.route('/weather', methods=['GET'])
def get_weather():
    weather_requests_total.inc()  # Increment Prometheus counter
    city = request.args.get('city')

    if not city:
        return jsonify({"error": "Please provide a city name using ?city=CityName"}), 400

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "City not found or OpenWeather API error"}), 404

    data = response.json()
    result = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"]
    }
    return jsonify(result)

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# -----------------------------
# Main Entry (For Railway + Local)
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)