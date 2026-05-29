from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.engine import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    weather = relationship(
        "WeatherData",
        back_populates="city",
        uselist=False,
        cascade="all, delete-orphan"
    )


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), unique=True)
    temperature = Column(Float, nullable=True)
    feels_like = Column(Float, nullable=True)
    humidity = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    wind_kph = Column(Float, nullable=True)
    pressure_mb = Column(Float, nullable=True)
    cloud = Column(Integer, nullable=True)
    uv = Column(Float, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

    city = relationship(
        "City",
        back_populates="weather"
    )
