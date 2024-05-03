from pydantic import BaseModel
from app.database.connexion import Base, engine

from typing import Optional
from sqlalchemy import Column, Integer, String, Float


class WeatherDB(Base):
    # Table Weather
    __tablename__ = 'weather'
    weather_id = Column(Integer, primary_key=True, index=True, unique=True)
    weather_name = Column(String, unique=True)
    weather_level = Column(Integer)
    weather_pound = Column(Float)


Base.metadata.create_all(bind=engine)


class WeatherBase(BaseModel):
    weather_id: int
    weather_name: str
    weather_level: int
    weather_pound: float


class WeatherCreate(WeatherBase):
    weather_id: Optional[int] = None
    weather_name: str
    weather_level: int
    weather_pound: Optional[float] = None


class WeatherUpdate(WeatherBase):
    weather_id: Optional[int] = None
    weather_name: Optional[str] = None
    weather_level: Optional[int] = None
    weather_pound: Optional[float] = None


class WeatherView(WeatherBase):
    ...


def get_all_weathers(db):
    return db.query(WeatherDB).all()


def get_weather_by_id(db, weather_id: int):
    return db.query(WeatherDB).filter(WeatherDB.weather_id == weather_id).first()


def get_weather_by_name(db, weather_name: str):
    return db.query(WeatherDB).filter(WeatherDB.weather_name == weather_name).first()


def post_weather(db, weather: WeatherCreate):
    db_weather = WeatherDB(**weather.model_dump(exclude_unset=True))
    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)
    return db_weather


def delete_weather(db, weather_id: int):
    db.query(WeatherDB).filter(WeatherDB.weather_id == weather_id).delete()
    db.commit()
    return {"message": "Weather deleted successfully."}


def patch_weather(db, weather_id: int, weather: WeatherUpdate):
    db_weather = db.query(WeatherDB).filter(WeatherDB.weather_id == weather_id).update(weather.model_dump(exclude_unset=True))
    db.commit()
    return db.query(WeatherDB).filter(WeatherDB.weather_id == weather_id).first()