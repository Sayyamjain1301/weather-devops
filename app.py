from flask import Flask, request, jsonify
import google.generativeai as genai
import requests
from dotenv import load_dotenv
import os

# Load .env if running locally
load_dotenv()

app = Flask(__name__)

# Get API keys from environment
GEMINI_KEY = os.getenv("GEMINI_KEY")
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")

if not GEMINI_KEY or not OPENWEATHER_KEY:
    raise ValueError("❌ Missing API keys! Please check your .env or Railway variables.")

# Configure Gemini
genai.configure(api_key=GEMINI_KEY)

# ✅ Home route (so Railway doesn't show 404)
@app.route("/")
def home():
    return "✅ Flask + Gemini + Weather API is running successfully on Railway!"

# ✅ Weather route
@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City parameter is missing"}), 400

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"
    try:
        res = requests.get(url)
        data = res.json()

        if data.get("cod") != 200:
            return jsonify({"error": data.get("message", "Unable to fetch weather")}), 400

        return jsonify({
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "condition": data["weather"][0]["description"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Gemini AI route
@app.route("/ask", methods=["POST"])
def ask_gemini():
    try:
        user_input = request.json.get("question")
        if not user_input:
            return jsonify({"error": "Question is required"}), 400

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_input)
        return jsonify({"answer": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Railway sets PORT automatically
    app.run(host="0.0.0.0", port=port, debug=True)