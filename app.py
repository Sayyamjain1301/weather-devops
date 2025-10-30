from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# API Keys
GEMINI_KEY = os.getenv("GEMINI_KEY")
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")

if not GEMINI_KEY or not OPENWEATHER_KEY:
    raise ValueError("⚠️ Missing API keys! Check your .env file.")

# Configure Gemini
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-pro")

# --- ROUTES ---

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        prompt = data.get("prompt")
        response = model.generate_content(prompt)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/weather", methods=["GET"])
def weather():
    city = request.args.get("city", "Pune")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"
    res = requests.get(url).json()
    if res.get("cod") != 200:
        return jsonify({"error": res.get("message", "City not found")})
    return jsonify({
        "city": res["name"],
        "temperature": res["main"]["temp"],
        "description": res["weather"][0]["description"]
    })

if __name__ == "__main__":
    app.run(debug=True)