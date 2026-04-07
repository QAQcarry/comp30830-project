from flask import jsonify
from flask_login import login_required
from sqlalchemy import text
from . import api_bp
from ..db import get_db


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
        rows = conn.execute(text("""
            SELECT number, available_bikes, available_bike_stands
            FROM (
                SELECT number, available_bikes, available_bike_stands,
                       ROW_NUMBER() OVER (PARTITION BY number ORDER BY last_update DESC, id DESC) AS rn
                FROM availability
            ) ranked
            WHERE rn = 1;
        """))
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
            text("""
                SELECT number, bike_stands, available_bike_stands,
                       available_bikes, status, last_update, scrape_time
                FROM availability
                WHERE number = :station_id
                ORDER BY last_update DESC, id DESC
                LIMIT 1;
            """),
            {"station_id": station_id}
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
            text("""
                SELECT available_bikes, available_bike_stands, last_update
                FROM availability
                WHERE number = :station_id
                ORDER BY last_update DESC
                LIMIT 48;
            """),
            {"station_id": station_id}
        )
        for row in rows:
            data.append(dict(row._mapping))
    return jsonify(history=data)


@api_bp.route("/weather")
@login_required
def get_weather():
    """Return the most recent weather record."""
    engine = get_db()
    data = []
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                SELECT temp, feels_like, humidity, wind_speed,
                       main, description, icon, scrape_time
                FROM weather
                ORDER BY scrape_time DESC
                LIMIT 1;
            """)
        )
        for row in rows:
            data.append(dict(row._mapping))
    return jsonify(weather=data)
