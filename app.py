from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests
import google.generativeai as genai

# ✅ Load environment variables
env_path = os.path.join(os.path.dirname(__file__), ".env")
print(f"Loading .env from: {env_path}")
load_dotenv(dotenv_path=env_path, override=True)

# ✅ API Keys
GEMINI_KEY = os.getenv("GEMINI_KEY")
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")

print("Gemini Key loaded:", bool(GEMINI_KEY))
print("OpenWeather Key loaded:", bool(OPENWEATHER_KEY))

if not GEMINI_KEY or not OPENWEATHER_KEY:
    raise ValueError("❌ Missing API keys in .env file. Please check GEMINI_KEY and OPENWEATHER_KEY.")

# ✅ Configure Gemini
genai.configure(api_key=GEMINI_KEY)

app = Flask(__name__)


# 🌦️ WEATHER API ROUTE
@app.route("/weather")
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City is required"}), 400

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"
        data = requests.get(url).json()

        if data.get("cod") != 200:
            return jsonify({"error": data.get("message", "City not found")}), 404

        weather = {
            "city": data["name"],
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"],
            "desc": data["weather"][0]["description"],
        }
        return jsonify(weather)
    except Exception as e:
        print("❌ Weather route error:", str(e))
        return jsonify({"error": str(e)}), 500


# 🧠 AI ASSISTANT ROUTE
@app.route("/ask", methods=["POST"])
def ask_ai():
    try:
        data = request.get_json()
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"error": "Question is required"}), 400

        print(f"\n🧠 User Question: {question}")

        # STEP 1: Ask Gemini to extract the city name
        city_extractor = genai.GenerativeModel("models/gemini-2.5-flash")
        city_prompt = f"Extract only the city name from this question: '{question}'. If no city is mentioned, return 'None'."
        city_response = city_extractor.generate_content(city_prompt)

        city_name = city_response.text.strip()
        print(f"🏙️ Gemini detected city: {city_name}")

        weather_info = ""
        if city_name.lower() != "none":
            # STEP 2: Fetch weather data for that city
            try:
                w_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHER_KEY}&units=metric"
                w_res = requests.get(w_url).json()

                if w_res.get("cod") == 200:
                    desc = w_res["weather"][0]["description"]
                    temp = w_res["main"]["temp"]
                    humidity = w_res["main"]["humidity"]
                    weather_info = (
                        f"The current weather in {city_name.title()} is {desc} "
                        f"with {temp}°C temperature and humidity around {humidity}%."
                    )
                else:
                    weather_info = f"I couldn't fetch live weather for {city_name}."
            except Exception as e:
                weather_info = f"⚠️ Weather lookup failed: {str(e)}"

        else:
            weather_info = "No city detected in your question."

        # STEP 3: Send question + weather info to Gemini for smart response
        final_prompt = f"""
        User asked: {question}
        Context: {weather_info}
        Give a short, natural reply based on current weather and user intent.
        """

        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(final_prompt)

        answer = ""
        if hasattr(response, "text") and response.text:
            answer = response.text.strip()
        elif hasattr(response, "candidates") and len(response.candidates) > 0:
            answer = response.candidates[0].content.parts[0].text.strip()
        else:
            answer = "⚠️ Gemini returned an empty response."

        print("✅ Gemini Final Response:", answer)
        return jsonify({"reply": answer})

    except Exception as e:
        import traceback
        traceback.print_exc()
        print("❌ AI route error:", str(e))
        return jsonify({"error": f"AI error: {str(e)}"}), 500


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    print("\n🌍 Starting Weather + AI Assistant on port 10000...")
    app.run(host="0.0.0.0", port=10000, debug=True)