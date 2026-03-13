from flask import jsonify, current_app, g
from sqlalchemy import create_engine, text
from . import api_bp


def get_db():
    """Return a SQLAlchemy engine, cached on Flask's g object per request."""
    if "_db_engine" not in g:
        cfg = current_app.config
        connection_string = "mysql+pymysql://{}:{}@{}:{}/{}".format(
            cfg["DB_USER"], cfg["DB_PASSWORD"],
            cfg["DB_HOST"], cfg["DB_PORT"], cfg["DB_NAME"]
        )
        g._db_engine = create_engine(connection_string)
    return g._db_engine


@api_bp.teardown_app_request
def teardown_db(exception):
    engine = g.pop("_db_engine", None)
    if engine is not None:
        engine.dispose()


@api_bp.route("/stations")
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


@api_bp.route("/weather")
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
