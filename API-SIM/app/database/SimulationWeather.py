from pydantic import BaseModel
from app.database.connexion import Base, engine
from app.database.Weather import WeatherView
from app.database.Simulation import SimulationView
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, backref



class SimulationWeatherDB(Base):
    # Table SimulationWeather
    __tablename__ = 'simulation_weather'
    simulation_id = Column(Integer, ForeignKey('simulation.simulation_id'), primary_key=True)
    simulation = relationship("SimulationDB", backref=backref("simulation_weather", cascade="all, delete-orphan"))
    weather_id = Column(Integer, ForeignKey('weather.weather_id'), primary_key=True)
    weather = relationship("WeatherDB", backref=backref("simulation_weather", cascade="all, delete-orphan"))



Base.metadata.create_all(bind=engine)


class SimulationWeatherBase(BaseModel):
    simulation_id: int
    weather_id: int


class SimulationWeatherCreate(SimulationWeatherBase):
    ...


class SimulationWeatherViewID(SimulationWeatherBase):
    simulation_id: int
    weather_id: int

class SimulationWeatherView(BaseModel):
    simulation: Optional[SimulationView] = []
    weather: Optional[WeatherView] = []


def get_all_simulation_weathers(db):
    return db.query(SimulationWeatherDB).all()


def get_simulation_weather_by_id(db, simulation_id: int, weather_id: int):
    return (db.query(SimulationWeatherDB).
            filter(SimulationWeatherDB.simulation_id == simulation_id).
            filter(SimulationWeatherDB.weather_id == weather_id).first())


def get_simulation_weather_by_simulation_id(db, simulation_id: int):
    return db.query(SimulationWeatherDB).filter(SimulationWeatherDB.simulation_id == simulation_id).all()


def get_simulation_weather_by_weather_id(db, weather_id: int):
    return db.query(SimulationWeatherDB).filter(SimulationWeatherDB.weather_id == weather_id).all()


def post_simulation_weather(db, simulation_weather: SimulationWeatherCreate):
    db_simulation_weather = SimulationWeatherDB(**simulation_weather.model_dump(exclude_unset=True))
    db.add(db_simulation_weather)
    db.commit()
    db.refresh(db_simulation_weather)
    return db_simulation_weather


def delete_simulation_weather(db, simulation_id: int, weather_id: int):
    db.query(SimulationWeatherDB).filter(SimulationWeatherDB.simulation_id == simulation_id).filter(SimulationWeatherDB.weather_id == weather_id).delete()
    db.commit()
    return {"message": "SimulationWeather deleted"}