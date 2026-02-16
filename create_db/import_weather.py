import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db import Weather

# 1. Database Configuration
DB_URL = "mysql+pymysql://root:PASSWORD@localhost:3306/bikes_database"
# (Update 'PASSWORD' with your local MySQL password)

# 2. Data Directory
# This is just my folder naming...
WEATHER_DIR = "weather_data"


def import_weather():
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    print(f"Starting scan of directory: {WEATHER_DIR} ...")

    file_count = 0
    record_count = 0

    # Check if directory exists
    if not os.path.exists(WEATHER_DIR):
        print(
            f"Error: Folder '{WEATHER_DIR}' not found. Please run this script from the project root."
        )
        return

    for root, dirs, files in os.walk(WEATHER_DIR):
        for filename in files:
            # Attempt to read all non-hidden files (some API data might be saved as timestamps)
            if not filename.startswith("."):
                file_path = os.path.join(root, filename)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        # Try parsing JSON
                        try:
                            data = json.load(f)
                        except json.JSONDecodeError:
                            continue  # Skip if not valid JSON

                        # Validate weather data format (must contain 'main' and 'weather')
                        if "main" not in data or "weather" not in data:
                            continue

                        # Map fields to Weather table columns
                        weather_record = Weather(
                            dt=data.get("dt"),
                            # Core data
                            temp=data["main"]["temp"],
                            feels_like=data["main"].get("feels_like"),
                            humidity=data["main"]["humidity"],
                            pressure=data["main"]["pressure"],
                            # Wind & Clouds
                            wind_speed=data.get("wind", {}).get("speed"),
                            wind_deg=data.get("wind", {}).get("deg"),
                            clouds_all=data.get("clouds", {}).get("all"),
                            # Description
                            main=data["weather"][0]["main"],
                            description=data["weather"][0]["description"],
                            icon=data["weather"][0]["icon"],
                        )

                        session.add(weather_record)
                        record_count += 1
                        file_count += 1

                        if record_count % 50 == 0:
                            session.commit()
                            print(
                                f"[Weather] Imported {file_count} files (Total records: {record_count})..."
                            )

                except Exception as e:
                    print(f"Error processing file {filename}: {e}")
                    session.rollback()

    session.commit()
    session.close()
    print("-" * 30)
    print(f"Weather data import completed!")
    print(f"Files processed: {file_count}")
    print(f"Total records: {record_count}")


if __name__ == "__main__":
    import_weather()
