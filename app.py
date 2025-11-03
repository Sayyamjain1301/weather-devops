from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
import requests
import os

# ✅ Load environment variables
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path, override=True)

# ✅ Read API keys
GEMINI_KEY = os.getenv("GEMINI_KEY")
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")

print("Gemini Key loaded:", bool(GEMINI_KEY))
print("OpenWeather Key loaded:", bool(OPENWEATHER_KEY))

if not GEMINI_KEY or not OPENWEATHER_KEY:
    raise ValueError("⚠️ Missing API keys! Check your .env file.")

# ✅ Configure Gemini
genai.configure(api_key=GEMINI_KEY)

# ✅ Initialize Flask
app = Flask(__name__)

# 🌤️ HOME PAGE
@app.route("/")
def home():
    return "<h1>🌦️ Weather + AI Assistant is Running!</h1><p>Use /weather or /ask endpoints.</p>"

# 🌦️ WEATHER ENDPOINT
@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City name required"}), 400

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"
    res = requests.get(url)
    data = res.json()

    if data.get("cod") != 200:
        return jsonify({"error": data.get("message", "City not found")}), 400

    weather_info = {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"].capitalize(),
        "lat": data["coord"]["lat"],
        "lon": data["coord"]["lon"]
    }

    return jsonify(weather_info)

# 🧠 GEMINI AI ENDPOINT
@app.route("/ask", methods=["POST"])
def ask_gemini():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "").strip()

        if not prompt:
            return jsonify({"error": "Prompt required"}), 400

        model = genai.GenerativeModel("models/gemini-2.0-flash")
        response = model.generate_content(prompt)

        if hasattr(response, "text") and response.text:
            reply = response.text.strip()
        elif hasattr(response, "candidates") and response.candidates:
            reply = response.candidates[0].content.parts[0].text.strip()
        else:
            reply = "⚠️ No clear response from Gemini."

        return jsonify({"response": reply})

    except Exception as e:
        print("❌ Gemini Error:", e)
        return jsonify({"error": str(e)}), 500

# 🚀 RUN SERVER (works for Railway)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🌍 Starting Weather + AI Assistant on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=True)