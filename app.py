from flask import Flask, render_template, request, jsonify
import requests
import google.generativeai as genai
from dotenv import load_dotenv
import os

# ----------------------------
# 1️⃣ Load environment variables
# ----------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# ----------------------------
# 2️⃣ Configure Gemini API
# ----------------------------
genai.configure(api_key=GEMINI_API_KEY)

# ----------------------------
# 3️⃣ Initialize Flask app
# ----------------------------
app = Flask(__name__)

# ----------------------------
# 4️⃣ Home route
# ----------------------------
@app.route('/')
def home():
    return "<h2>✅ Flask + Gemini + Weather API is running on port 5001!</h2>"

# ----------------------------
# 5️⃣ Route to get weather data
# ----------------------------
@app.route('/weather', methods=['POST'])
def get_weather():
    try:
        city = request.json.get("city")
        if not city:
            return jsonify({"error": "City name is required"}), 400

        # Fetch weather from OpenWeatherMap API
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(weather_url)
        data = response.json()

        if data.get("cod") != 200:
            return jsonify({"error": f"City '{city}' not found"}), 404

        weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].capitalize()
        }

        return jsonify(weather_info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------------------------
# 6️⃣ Route for Gemini AI analysis
# ----------------------------
@app.route('/analyze', methods=['POST'])
def analyze_weather():
    try:
        data = request.json
        weather_text = data.get("weather_text")

        if not weather_text:
            return jsonify({"error": "Missing 'weather_text'"}), 400

        # Generate AI response
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Explain this weather report in simple terms: {weather_text}")

        return jsonify({"ai_response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------------------------
# 7️⃣ Run app on port 5001
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)