from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests
import google.generativeai as genai

# ---------------------------------------------------------------------
# ✅ Load environment variables
# ---------------------------------------------------------------------
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path, override=True)

GEMINI_KEY = os.getenv("GEMINI_KEY")
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")

# Validate keys
if not GEMINI_KEY or not OPENWEATHER_KEY:
    raise ValueError("⚠️ Missing GEMINI_KEY or OPENWEATHER_KEY in .env file")

# ---------------------------------------------------------------------
# ✅ Configure Gemini
# ---------------------------------------------------------------------
genai.configure(api_key=GEMINI_KEY)

# ---------------------------------------------------------------------
# ✅ Initialize Flask
# ---------------------------------------------------------------------
app = Flask(__name__)

# ---------------------------------------------------------------------
# 🏠 Home Route
# ---------------------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------------------------------------------------------------
# 🌦️ Weather API Route
# ---------------------------------------------------------------------
@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City name required"}), 400

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"
        res = requests.get(url)
        data = res.json()

        if data.get("cod") != 200:
            return jsonify({"error": data.get("message", "Unable to fetch weather")}), 400

        # Format clean JSON for frontend
        result = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"].capitalize(),
            "lat": data["coord"]["lat"],
            "lon": data["coord"]["lon"]
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------------------------------
# 🤖 Gemini AI Assistant Route
# ---------------------------------------------------------------------
@app.route("/ask_gemini", methods=["POST"])
def ask_gemini():
    try:
        data = request.get_json()
        question = data.get("question", "")

        if not question:
            return jsonify({"error": "Question is required"}), 400

        # Use Gemini model
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(question)

        # Safely extract text
        answer = getattr(response, "text", None)
        if not answer and hasattr(response, "candidates"):
            answer = response.candidates[0].content.parts[0].text.strip()

        return jsonify({"response": answer or "⚠️ No clear response from Gemini."})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"AI Error: {str(e)}"}), 500

# ---------------------------------------------------------------------
# 🟢 Main Entry Point
# ---------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Railway/Render uses dynamic PORT
    print(f"🌍 Starting Weather + AI Assistant on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=True)