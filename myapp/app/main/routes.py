from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
import os
import requests
import joblib
from datetime import datetime

main_bp = Blueprint("main", __name__)

# Load model once on startup
basedir = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(basedir, "..", "ml", "bike_availability_model.pkl")
try:
    bike_model = joblib.load(MODEL_PATH)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Failed to load model: {e}")
    bike_model = None


@main_bp.route("/")
def index():
    return render_template("main/welcome.html")


@main_bp.route("/map")
def map_view():
    google_maps_key = os.environ.get("GOOGLE_MAPS_KEY", "")
    return render_template("main/index.html", google_maps_key=google_maps_key)


@main_bp.route("/predict", methods=["POST"])
def predict_availability():
    if not bike_model:
        return jsonify({"error": "Model unavailable"}), 500

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    station_id = data.get("station_id")
    date_str = data.get("date")
    time_str = data.get("time")

    if not all([station_id, date_str, time_str]):
        return jsonify({"error": "Missing required fields"}), 400

    # Extract hour and day_of_week
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        hour = dt.hour
        day_of_week = dt.weekday()
    except ValueError:
        return jsonify({"error": "Invalid format. Use YYYY-MM-DD and HH:MM"}), 400

    try:
        api_key = os.environ.get("OPENWEATHER_API_KEY")
        if not api_key:
            raise ValueError("Missing OPENWEATHER_API_KEY")

        # Fetch live weather for Dublin
        url = f"http://api.openweathermap.org/data/2.5/weather?q=Dublin,IE&appid={api_key}&units=metric"
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        weather_data = response.json()
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        pressure = weather_data["main"]["pressure"]

    except Exception as e:
        # Fallback dummy data if API fails
        print(f"Weather API fallback triggered: {e}")
        temperature = 12.5
        humidity = 75.0
        pressure = 1010.0

    # Feature order: station_id, temp, humidity, pressure, hour, day_of_week
    features = [[station_id, temperature, humidity, pressure, hour, day_of_week]]

    try:
        prediction = bike_model.predict(features)[0]

        # Apply business rules
        status = "Likely available" if prediction >= 1 else "Unlikely available"

        final_bikes = max(0, int((float(prediction))))

        return jsonify(
            {
                "station_id": station_id,
                "predicted_bikes": final_bikes,
                "availability_status": status,
                "message": "Success",
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
