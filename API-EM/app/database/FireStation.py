from pydantic import BaseModel
from app.database.connection import Base, engine
from sqlalchemy import Column, Float, String, Integer
from typing import Optional
from app.database.DataBaseFunction import DataBaseRequest
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict


class FireStationDB(Base):
    # Table FireStation
    __tablename__ = 'firestation'
    id_fire_station = Column(Integer, primary_key=True, index=True)
    fire_station_name = Column(String(50), unique=True)
    fire_station_longitude = Column(Float)
    fire_station_latitude = Column(Float)


Base.metadata.create_all(bind=engine)


class FireStationView(BaseModel):
    fire_station_name: str
    fire_station_longitude: Optional[float] = None
    fire_station_latitude: Optional[float] = None


class FireStationInDB(FireStationView):
    id_fire_station: Optional[int] = None




def get_all_fire_stations(db):
    return DataBaseRequest.get_all_data(db, FireStationDB)


def get_fire_station_by_id(db, id_fire_station: int):
    return DataBaseRequest.get_data_by_something(db, FireStationDB, FireStationDB.id_fire_station == id_fire_station )


def get_fire_station_by_name(db, fire_station_name: str):
    return DataBaseRequest.get_data_by_something(db, FireStationDB, FireStationDB.fire_station_name == fire_station_name.lower())


def post_fire_station(db, fire_station: FireStationView):
    db_fire_station = FireStationDB(**fire_station.model_dump())
    return DataBaseRequest.post_data(db, db_fire_station)


def delete_fire_station(db, id_fire_station: int):
    DataBaseRequest.delete_data(db, FireStationDB, FireStationDB.id_fire_station == id_fire_station)
    return True