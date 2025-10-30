from flask import Flask, request, jsonify, render_template
import requests
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load API keys
GEMINI_KEY = os.getenv("GEMINI_KEY")
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")

# Check for missing keys
if not GEMINI_KEY or not OPENWEATHER_KEY:
    raise ValueError("⚠️ Missing API keys! Check your .env file.")

# Configure Gemini AI
genai.configure(api_key=GEMINI_KEY)

# Flask app
app = Flask(__name__)

# 🔹 Home route
@app.route('/')
def home():
    return render_template('index.html')


# 🔹 Weather route
@app.route('/weather', methods=['POST'])
def get_weather():
    try:
        city = request.form['city']
        print(f"🌤 Fetching weather for: {city}")
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"

        res = requests.get(weather_url)
        data = res.json()
        print("📦 API Response:", data)

        if data.get("cod") != 200:
            return jsonify({"error": data.get("message", "Error fetching weather")}), 400
        
        return jsonify(data)
    
    except Exception as e:
        print("❌ Weather route error:", e)
        return jsonify({"error": str(e)}), 500


# 🔹 Gemini AI Assistant route
@app.route('/assistant_ai', methods=['POST'])
def ai_assistant():
    try:
        user_prompt = request.form['prompt']
        print(f"🤖 User asked: {user_prompt}")

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_prompt)

        return jsonify({"response": response.text})
    
    except Exception as e:
        print("❌ Gemini route error:", e)
        return jsonify({"error": str(e)}), 500


# 🔹 Run the Flask app
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=10000, debug=True)