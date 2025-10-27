from flask import Flask, render_template, request
import requests, os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    weather_condition = None

    if request.method == "POST":
        city = request.form["city"]
        api_key = os.getenv("WEATHER_API_KEY")

        if not api_key:
            return "❌ Error: WEATHER_API_KEY not found. Set it in Render Environment Variables."

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            weather = response.json()
            weather_condition = weather["weather"][0]["main"].lower()

    return render_template("index.html", weather=weather, condition=weather_condition)

if __name__ == "__main__":
    app.run(debug=True)