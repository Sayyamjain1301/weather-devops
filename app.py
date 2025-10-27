from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    if request.method == "POST":
        city = request.form["city"]
        api_key = os.getenv("WEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            weather = response.json()
    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)