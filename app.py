from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import requests
import os
from dotenv import load_dotenv
from waitress import serve

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load API keys from .env
GEMINI_KEY = os.getenv("GEMINI_KEY")
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_KEY)

# Root route
@app.route("/")
def home():
    return "<h2>✅ Flask + Gemini + Weather API is running successfully on Railway!</h2>"

# Route to get weather data
@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City name is required"}), 400

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "City not found"}), 404

    data = response.json()
    weather = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"]
    }

    return jsonify(weather)

# Route for AI (Gemini) chat
@app.route("/ask_gemini", methods=["POST"])
def ask_gemini():
    try:
        user_input = request.json.get("question")
        if not user_input:
            return jsonify({"error": "Question is required"}), 400

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_input)

        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Entry point
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🌍 Starting Weather + Gemini AI app on port {port}")
    serve(app, host="0.0.0.0", port=port)