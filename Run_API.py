from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

JCDECAUX_API_KEY = os.getenv("JCDECAUX_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

CITY_NAME = os.getenv("OPENWEATHER_CITY", "Dublin,IE")
CONTRACT_NAME = os.getenv("JCDECAUX_CONTRACT", "dublin")

JCDECAUX_URL = "https://api.jcdecaux.com/vls/v1/stations"
OWM_CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
OWM_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


@app.route("/")
def home():
    return jsonify(message="API is running", endpoints=["/api/bikes", "/api/weather"])


@app.route("/api/bikes")
def bikes():
    if not JCDECAUX_API_KEY:
        return jsonify(error="Missing environment variable JCDECAUX_API_KEY"), 500

    r = requests.get(
        JCDECAUX_URL,
        params={"contract": CONTRACT_NAME, "apiKey": JCDECAUX_API_KEY},
        timeout=20,
    )
    if not r.ok:
        return jsonify(error="JCDecaux request failed", status=r.status_code, body=r.text[:200]), 502

    return jsonify(r.json())


@app.route("/api/weather")
def weather():
    if not OPENWEATHER_API_KEY:
        return jsonify(error="Missing environment variable OPENWEATHER_API_KEY"), 500

    cur = requests.get(
        OWM_CURRENT_URL,
        params={"q": CITY_NAME, "appid": OPENWEATHER_API_KEY, "units": "metric"},
        timeout=20,
    )
    if not cur.ok:
        return jsonify(error="OpenWeather current request failed", status=cur.status_code, body=cur.text[:200]), 502

    fc = requests.get(
        OWM_FORECAST_URL,
        params={"q": CITY_NAME, "appid": OPENWEATHER_API_KEY, "units": "metric"},
        timeout=20,
    )
    if not fc.ok:
        return jsonify(error="OpenWeather forecast request failed", status=fc.status_code, body=fc.text[:200]), 502

    return jsonify(city=CITY_NAME, current=cur.json(), forecast=fc.json())


if __name__ == "__main__":
    app.run(debug=True)
