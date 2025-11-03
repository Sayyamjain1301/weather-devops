import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
import requests

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print(f"✅ Loaded .env from: {dotenv_path}")
else:
    print("⚠️ No .env file found!")

# Initialize Flask
app = Flask(__name__)

# Get API keys from .env
GEMINI_KEY = os.getenv("GEMINI_KEY")
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")

if not GEMINI_KEY or not OPENWEATHER_KEY:
    raise ValueError("❌ Missing API keys! Check your .env file.")

# Configure Gemini
genai.configure(api_key=GEMINI_KEY)

# 🌍 Home Route
@app.route("/")
def home():
    return render_template("index.html")

# 🌤 Weather API Route
@app.route("/weather", methods=["POST"])
def get_weather():
    try:
        city = request.form["city"]
        print(f"🌤 Fetching weather for: {city}")

        weather_url = (
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"
        )
        res = requests.get(weather_url)
        data = res.json()

        if data.get("cod") != 200:
            return jsonify({"error": data.get("message", "Error fetching weather")}), 400

        print("✅ Weather Data:", data)
        return jsonify(data)
    except Exception as e:
        print("❌ Error in /weather:", str(e))
        return jsonify({"error": str(e)}), 500

# 🤖 Gemini AI Assistant Route
@app.route("/assistant_ai", methods=["POST"])
def assistant_ai():
    try:
        data = request.get_json()
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"error": "Empty prompt!"}), 400

        print(f"🧠 Gemini Prompt: {question}")

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(question)

        if not response or not response.text:
            return jsonify({"error": "No response from Gemini"}), 500

        print("✅ Gemini Response:", response.text)
        return jsonify({"answer": response.text})

    except Exception as e:
        print("❌ Gemini Error:", str(e))
        return jsonify({"error": str(e)}), 500


# ✅ Run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Railway/Render will auto-assign PORT
    print(f"🌍 Starting Weather + AI Assistant on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=True)