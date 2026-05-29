from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import schemas
import crud
from db.engine import get_db
from worker.tasks.weather_tasks import update_weather_for_city

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "FastAPI is running"
    }


@app.post(
    "/cities",
    response_model=schemas.CityResponse
)
def add_city(
    city_data: schemas.CityCreate,
    db: Session = Depends(get_db)
):
    existing_city = crud.get_city_by_name(
        db,
        city_data.name
    )

    if existing_city:
        raise HTTPException(
            status_code=400,
            detail="City already exists"
        )

    city = crud.create_city(
        db,
        city_data.name
    )

    update_weather_for_city.delay(city.id)

    return city


@app.get(
    "/cities",
    response_model=list[schemas.CityResponse]
)
def list_cities(
    db: Session = Depends(get_db)
):
    return crud.get_cities(db)


@app.post("/cities/{city_id}/refresh")
def refresh_weather(
    city_id: int,
    db: Session = Depends(get_db)
):
    city = crud.get_city(
        db,
        city_id
    )

    if not city:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )

    update_weather_for_city.delay(city.id)

    return {
        "message": "Weather update task started",
        "city_id": city.id
    }
