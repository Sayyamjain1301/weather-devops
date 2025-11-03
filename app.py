from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

app = Flask(__name__)

# Load API keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

# 🌦️ Weather API Route
@app.route('/get_weather', methods=['POST'])
def get_weather():
    try:
        data = request.get_json()
        city = data.get('city')

        if not city:
            return jsonify({'error': 'City name is required'}), 400

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        weather_data = response.json()

        if weather_data.get('cod') != 200:
            return jsonify({'error': 'City not found'}), 404

        result = {
            'city': weather_data['name'],
            'temperature': weather_data['main']['temp'],
            'description': weather_data['weather'][0]['description'],
            'latitude': weather_data['coord']['lat'],
            'longitude': weather_data['coord']['lon']
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 🤖 Gemini AI Chat Route (optional)
@app.route('/ask', methods=['POST'])
def ask():
    try:
        question = request.get_json().get('question', '')
        if not question:
            return jsonify({'error': 'Question cannot be empty'}), 400
        # Mock AI Response (replace this later with Gemini API integration)
        ai_response = f"AI Response to: '{question}' (Gemini API integration here)"
        return jsonify({'answer': ai_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 🌍 Auto-Center Map on user's location
@app.route('/get_location')
def get_location():
    try:
        ipinfo_url = "https://ipinfo.io/json"
        response = requests.get(ipinfo_url)
        data = response.json()
        loc = data.get('loc', '0,0').split(',')
        latitude, longitude = loc[0], loc[1]
        return jsonify({'latitude': latitude, 'longitude': longitude})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ✅ Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)