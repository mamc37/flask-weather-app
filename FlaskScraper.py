from flask import Flask, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import waitress

app = Flask(__name__)

def get_weather():
    url = "https://www.accuweather.com/en/us/irvine/92612/current-weather/337095"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract weather condition
    weather_element = soup.find("div", class_="phrase")
    weather = weather_element.text.strip() if weather_element else "N/A"

    # Extract temperature
    temp_element = soup.find("div", class_="display-temp")
    temperature = temp_element.text.strip() if temp_element else "N/A"

    # Extract humidity safely
    humidity = "N/A"
    details = soup.find_all("div", class_="detail-item spaced-content")
    for detail in details:
        if "Humidity" in detail.text:
            humidity = detail.find_all("div")[1].text.strip()
            break

    return {"weather": weather, "temperature": temperature, "humidity": humidity}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather", methods=["GET"])
def weather():
    weather = get_weather()
    return render_template("weather.html", weather=weather)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=10000)

