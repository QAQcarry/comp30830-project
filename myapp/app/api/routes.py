from flask import jsonify
from flask_login import login_required
from sqlalchemy import text
from . import api_bp
from ..db import get_db
import os
import requests


@api_bp.route("/stations")
@login_required
def get_stations():
    """Return all stations as JSON."""
    engine = get_db()
    stations = []
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM station;"))
        for row in rows:
            stations.append(dict(row._mapping))
    return jsonify(stations=stations)


@api_bp.route("/available/all")
@login_required
def get_all_availability():
    """Return the latest availability for every station (one row each)."""
    engine = get_db()
    data = []
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
            SELECT number, available_bikes, available_bike_stands
            FROM (
                SELECT number, available_bikes, available_bike_stands,
                       ROW_NUMBER() OVER (PARTITION BY number ORDER BY last_update DESC, id DESC) AS rn
                FROM availability
            ) ranked
            WHERE rn = 1;
        """
            )
        )
        for row in rows:
            data.append(dict(row._mapping))
    return jsonify(availability=data)


@api_bp.route("/available/<int:station_id>")
@login_required
def get_availability(station_id):
    """Return the latest availability for a given station."""
    engine = get_db()
    data = []
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
                SELECT number, bike_stands, available_bike_stands,
                       available_bikes, status, last_update, scrape_time
                FROM availability
                WHERE number = :station_id
                ORDER BY last_update DESC, id DESC
                LIMIT 1;
            """
            ),
            {"station_id": station_id},
        )
        for row in rows:
            data.append(dict(row._mapping))
    return jsonify(availability=data)


@api_bp.route("/available/<int:station_id>/history")
@login_required
def get_availability_history(station_id):
    """Return availability history for a given station."""
    engine = get_db()
    data = []
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
                SELECT available_bikes, available_bike_stands, last_update
                FROM availability
                WHERE number = :station_id
                ORDER BY last_update DESC
                LIMIT 48;
            """
            ),
            {"station_id": station_id},
        )
        for row in rows:
            data.append(dict(row._mapping))
    return jsonify(history=data)


@api_bp.route("/weather")
@login_required
def get_weather():
    try:
        api_key = os.environ.get("OPENWEATHER_API_KEY")
        if not api_key:
            raise ValueError("Missing OPENWEATHER_API_KEY")

        # Fetch live weather data
        url = f"http://api.openweathermap.org/data/2.5/weather?q=Dublin,IE&appid={api_key}&units=metric"
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        data = response.json()

        # Format data for frontend
        live_weather = [
            {
                "temp": data["main"]["temp"],
                "description": data["weather"][0]["description"].title(),
                "icon": data["weather"][0]["icon"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
            }
        ]

        return jsonify(weather=live_weather)

    except Exception as e:
        print(f"Weather fetch failed: {e}")
        # Fallback data on error
        fallback = [{"temp": 12.5, "description": "Error", "icon": "04d"}]
        return jsonify(weather=fallback)
