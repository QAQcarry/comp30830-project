import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db import Station

# Database configuration
DB_URL = "mysql+pymysql://root:PASSWORD@localhost:3306/bikes_database"
# Update 'PASSWORD' with your password

# Path to the static station data file
FILE_PATH = "stations.json"


def fill_static_data():
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Load JSON data
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"Found {len(data)} stations. Processing...")

        added_count = 0
        for item in data:
            # Check if station already exists to avoid duplicates
            exists = session.query(Station).filter_by(number=item["number"]).first()

            if not exists:
                new_station = Station(
                    number=item["number"],
                    name=item["name"],
                    address=item["address"],
                    latitude=item["position"]["lat"],
                    longitude=item["position"]["lng"],
                    banking=item["banking"],
                    bonus=item["bonus"],
                )
                session.add(new_station)
                added_count += 1

        session.commit()
        print(f"Success! Added {added_count} new stations.")

    except Exception as e:
        print(f" Error: {e}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    fill_static_data()
