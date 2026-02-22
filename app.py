from flask import Flask, g, render_template, jsonify
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

# Database Configuration 
USER = os.environ.get("DB_USER")
PASSWORD = os.environ.get("DB_PASSWORD")
PORT = os.environ.get("DB_PORT")
DB = os.environ.get("DB_NAME")
URI = os.environ.get("DB_HOST")

app = Flask(__name__, static_url_path='')


#  Database Connection 

def connect_to_db():
    """Create and return a SQLAlchemy engine."""
    connection_string = "mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB)
    engine = create_engine(connection_string, echo=True)
    return engine


def get_db():
    """Return the database engine, creating it if not already stored in Flask's g."""
    db_engine = getattr(g, '_database', None)
    if db_engine is None:
        db_engine = g._database = connect_to_db()
    return db_engine


@app.teardown_appcontext
def teardown_db(exception):
    """Clean up the database engine when the app context ends."""
    db_engine = getattr(g, '_database', None)
    if db_engine is not None:
        db_engine.dispose()


#  Routes 

@app.route('/')
def index():
    """Serve the main HTML page."""
    return render_template('index.html')


@app.route('/stations')
def get_stations():
    """Return all station info as JSON."""
    engine = get_db()
    stations = []
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM station;"))
        for row in rows:
            stations.append(dict(row._mapping))
    return jsonify(stations=stations)


@app.route('/available/<int:station_id>')
def get_availability(station_id):
    """Return the latest availability data for a given station as JSON."""
    engine = get_db()
    data = []
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                SELECT number, bike_stands, available_bike_stands,
                       available_bikes, status, last_update, scrape_time
                FROM availability
                WHERE number = :station_id
                ORDER BY scrape_time DESC
                LIMIT 1;
            """),
            {"station_id": station_id}
        )
        for row in rows:
            data.append(dict(row._mapping))
    return jsonify(availability=data)


#  Run 

if __name__ == '__main__':
    app.run(debug=True)
