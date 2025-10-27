from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    if request.method == "POST":
        city = request.form["city"]
        api_key = "909b2267739653e815172b6049d722f8"   # ✅ your real API key
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") == 200:
            weather = {
                "city": city.title(),
                "temp": round(data["main"]["temp"], 1),
                "description": data["weather"][0]["description"].title(),
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"],
                "icon": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
            }
        else:
            weather = {
                "city": "City not found!",
                "temp": "--",
                "description": "Try again."
            }

    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)