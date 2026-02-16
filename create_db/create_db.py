from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    BigInteger,
    Boolean,
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


# 1: Station


class Station(Base):
    __tablename__ = "station"

    number = Column(Integer, primary_key=True)
    name = Column(String(255))
    address = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    banking = Column(Boolean)
    bonus = Column(Boolean)

    # Establish a relationship with Availability
    availabilities = relationship("Availability", back_populates="station")


# 2: Availability


class Availability(Base):
    __tablename__ = "availability"

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer, ForeignKey("station.number"))  # Related to Station table

    bike_stands = Column(Integer)
    available_bike_stands = Column(Integer)
    available_bikes = Column(Integer)
    status = Column(String(50))

    last_update = Column(BigInteger)
    scrape_time = Column(DateTime, server_default=func.now())

    station = relationship("Station", back_populates="availabilities")


# 3: Weather (天气实时表)


class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, autoincrement=True)

    temp = Column(Float)
    feels_like = Column(Float)
    humidity = Column(Integer)
    pressure = Column(Integer)

    wind_speed = Column(Float)  # 对应 wind -> speed
    wind_deg = Column(Integer)  # 对应 wind -> deg
    clouds_all = Column(Integer)  # 对应 clouds -> all

    main = Column(String(50))  # 对应 weather[0] -> main (例如 "Clouds")
    description = Column(String(100))  # 对应 weather[0] -> description
    icon = Column(String(10))  # 对应 weather[0] -> icon

    # time
    dt = Column(BigInteger)
    scrape_time = Column(DateTime, server_default=func.now())


# Create table


DB_URL = "mysql+pymysql://root:PASSWORD@localhost:3306/bikes_database"
# USE YOUR PASSWORD

try:
    print("Connecting to database...")
    engine = create_engine(DB_URL)
    connection = engine.connect()
    print("Successfully connected to MySQL!")
    connection.close()

    print("Creating table structures (Station, Availability, Weather)...")
    Base.metadata.create_all(engine)
    print("Tables created successfully! Your database is ready to receive data.")

except Exception as e:
    print("Error occurred!")
    print(f"Error message: {e}")
    print(
        "Suggestion: Check if 1. Password is correct? 2. Database 'bikes_database' exists?"
    )
