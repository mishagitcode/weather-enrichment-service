from datetime import datetime

from db.engine import SessionLocal
from db.models import City, WeatherData
from services.weather_api import fetch_weather
from worker.celery_app import celery_app


@celery_app.task(name="worker.tasks.weather_tasks.update_weather_for_city")
def update_weather_for_city(city_id: int):
    db = SessionLocal()

    try:
        city = (
            db.query(City)
            .filter(City.id == city_id)
            .first()
        )

        if not city:
            return {
                "status": "error",
                "message": "City not found"
            }

        weather = fetch_weather(city.name)

        weather_data = (
            db.query(WeatherData)
            .filter(WeatherData.city_id == city.id)
            .first()
        )

        if weather_data:
            weather_data.temperature = weather["temperature"]
            weather_data.feels_like = weather["feels_like"]
            weather_data.humidity = weather["humidity"]
            weather_data.description = weather["description"]
            weather_data.wind_kph = weather["wind_kph"]
            weather_data.pressure_mb = weather["pressure_mb"]
            weather_data.cloud = weather["cloud"]
            weather_data.uv = weather["uv"]
            weather_data.updated_at = datetime.utcnow()
        else:
            weather_data = WeatherData(
                city_id=city.id,
                temperature=weather["temperature"],
                feels_like=weather["feels_like"],
                humidity=weather["humidity"],
                description=weather["description"],
                wind_kph=weather["wind_kph"],
                pressure_mb=weather["pressure_mb"],
                cloud=weather["cloud"],
                uv=weather["uv"],
                updated_at=datetime.utcnow()
            )

            db.add(weather_data)

        db.commit()

        return {
            "status": "success",
            "city": city.name,
            "weather": weather
        }

    except Exception as error:
        db.rollback()

        return {
            "status": "error",
            "message": str(error)
        }

    finally:
        db.close()
