import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db import Availability

# 1. Database Configuration
DB_URL = "mysql+pymysql://root:PASSWORD@localhost:3306/bikes_database"
# Update 'PASSWORD' with your local MySQL password

# 2. Data Directory
# This is just my folder naming...
DATA_DIR = "data"


def import_bikes():
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    print(f"🚲 Starting scan of directory: {DATA_DIR} ...")

    file_count = 0
    record_count = 0

    # Check if directory exists
    if not os.path.exists(DATA_DIR):
        print(
            f"Error: Folder '{DATA_DIR}' not found. Please run this script from the project root."
        )
        return

    # Walk through the directory
    for root, dirs, files in os.walk(DATA_DIR):
        for filename in files:
            # Flexible check: accepts files with 'bikes' in name OR ending with .json
            if "bikes" in filename or filename.endswith(".json"):
                file_path = os.path.join(root, filename)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                        batch = []
                        for item in data:
                            record = Availability(
                                number=item["number"],
                                bike_stands=item["bike_stands"],
                                available_bike_stands=item["available_bike_stands"],
                                available_bikes=item["available_bikes"],
                                status=item["status"],
                                last_update=item["last_update"],
                            )
                            batch.append(record)

                        if batch:
                            session.add_all(batch)
                            session.commit()
                            record_count += len(batch)
                            file_count += 1

                            if file_count % 50 == 0:
                                print(f"[Bike] Imported {file_count} files...")

                except Exception as e:
                    print(f"Error processing file {filename}: {e}")
                    session.rollback()

    session.close()
    print("-" * 30)
    print(f"Bike data import completed!")
    print(f"Files processed: {file_count}")
    print(f"Total records: {record_count}")


if __name__ == "__main__":
    import_bikes()
