from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import requests
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, firestore

# Load environment variables
load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")
FIRESTORE_CRED_PATH = os.getenv("FIRESTORE_CRED_PATH")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "default_secret")

if not GEMINI_KEY or not OPENWEATHER_KEY:
    raise ValueError("⚠️ Missing API keys! Check your .env file.")

# Initialize Flask
app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

# Initialize Gemini
genai.configure(api_key=GEMINI_KEY)

# Initialize Firestore
if not firebase_admin._apps:
    cred = credentials.Certificate(FIRESTORE_CRED_PATH)
    firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City not provided"}), 400

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"
    res = requests.get(weather_url)
    data = res.json()

    if data.get("cod") != 200:
        return jsonify({"error": data.get("message", "Error fetching weather")}), 400

    weather_info = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
    }

    # Store to Firestore
    db.collection("weather_logs").add(weather_info)

    return jsonify(weather_info)

@app.route('/ask', methods=['POST'])
def ask_gemini():
    user_input = request.json.get("prompt")
    if not user_input:
        return jsonify({"error": "Prompt missing"}), 400

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_input)
        reply = response.text

        # Store in Firestore
        db.collection("chat_logs").add({
            "prompt": user_input,
            "response": reply
        })

        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)