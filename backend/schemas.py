from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CityCreate(BaseModel):
    name: str


class WeatherResponse(BaseModel):
    temperature: Optional[float]
    feels_like: Optional[float]
    humidity: Optional[int]
    description: Optional[str]

    wind_kph: Optional[float]
    pressure_mb: Optional[float]
    cloud: Optional[int]
    uv: Optional[float]

    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class CityResponse(BaseModel):
    id: int
    name: str
    weather: Optional[WeatherResponse] = None

    class Config:
        from_attributes = True
