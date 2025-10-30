import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_KEY"))

def generate_summary(weather_data):
    try:
        city = weather_data.get("city", "the city")
        temp = weather_data.get("temperature")
        humidity = weather_data.get("humidity")
        description = weather_data.get("description", "")
        
        prompt = f"""
        You are an AI weather assistant. Based on the given data, give a short, helpful forecast.

        City: {city}
        Temperature: {temp}°C
        Humidity: {humidity}%
        Condition: {description}

        Give a friendly 2-3 sentence summary, e.g.
        "It looks like Udaipur will have mild weather tomorrow with light showers likely in the evening."
        If rain-related words appear in the condition, mention chances of rain clearly.
        """

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        print("AI Summary Error:", e)
        return f"Error: {e}"