from sqlalchemy.orm import Session

from db.models import City


def create_city(db: Session, name: str) -> City:
    city = City(name=name)

    db.add(city)
    db.commit()
    db.refresh(city)

    return city


def get_cities(db: Session):
    return db.query(City).all()


def get_city(db: Session, city_id: int):
    return (
        db.query(City)
        .filter(City.id == city_id)
        .first()
    )


def get_city_by_name(db: Session, name: str):
    return (
        db.query(City)
        .filter(City.name == name)
        .first()
    )
