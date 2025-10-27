from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Load your API key securely from environment variable
api_key = os.getenv("WEATHER_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form["city"]

        # OpenWeatherMap API URL
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        response = requests.get(url)
        data = response.json()

        if data.get("cod") == 200:
            weather = {
                "city": data["name"],
                "temp": data["main"]["temp"],
                "description": data["weather"][0]["description"].title(),
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"],
                "icon": data["weather"][0]["icon"],
            }
        else:
            error = "City not found! Please try again."

    return render_template("index.html", weather=weather, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)