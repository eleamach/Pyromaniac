from pydantic import BaseModel
from app.database.connection import Base, engine
from sqlalchemy import Column, Float, String, Integer, DateTime, Boolean, ForeignKey
from typing import Optional, List
from app.database.DataBaseFunction import DataBaseRequest
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict
from app.database.SensorHisto import SensorHistoInDB, SensorHistoDB


class SensorDB  (Base):
    # Table Sensor
    __tablename__ = 'sensor'
    id_sensor = Column(Integer, primary_key=True, index=True)
    sensor_longitude = Column(Float)
    sensor_latitude = Column(Float)


Base.metadata.create_all(bind=engine)


class SensorView(BaseModel):
    sensor_longitude: float
    sensor_latitude: float


class SensorUpdate(SensorView):
    sensor_longitude: Optional[float] = None
    sensor_latitude: Optional[float] = None


class SensorInDB(SensorView):
    id_sensor: Optional[int] = None


class SensorWithHisto(SensorView):
    id_sensor: Optional[int] = None
    sensor_histo: List[SensorHistoInDB] = []


def get_all_sensors(db):
    return DataBaseRequest.get_all_data(db, SensorDB)


def get_sensor_by_id(db, id_sensor: int):
    db_sensor = db.query(SensorDB).filter(SensorDB.id_sensor == id_sensor).first()
    db_sensor = SensorWithHisto(**db_sensor.__dict__)
    db_sensor_histo = (db.query(SensorHistoDB).filter(SensorHistoDB.id_sensor == id_sensor).
                              filter(SensorHistoDB.sensor_histo_is_processed == True).order_by(SensorHistoDB.id_sensor_histo.desc()).first())
    db_sensor.sensor_histo.append(SensorHistoInDB(**db_sensor_histo.__dict__))
    return db_sensor


def get_sensor_by_coordinates(db, sensor_longitude: float, sensor_latitude: float):
    return db.query(SensorDB).filter(SensorDB.sensor_longitude == sensor_longitude,SensorDB.sensor_latitude == sensor_latitude).first()


def post_sensor(db, sensor: SensorView):
    db_sensor = SensorDB(**sensor.model_dump(exclude_unset=True))
    return DataBaseRequest.post_data(db, db_sensor)


def delete_sensor(db, id_sensor: int):
    DataBaseRequest.delete_data(db, SensorDB, SensorDB.id_sensor == id_sensor)
    return True


def update_sensor(db, id_sensor, sensor: SensorView):
    db.query(SensorDB).filter(SensorDB.id_sensor == id_sensor).update(sensor.model_dump(exclude_unset=True))
    db.commit()
    return db.query(SensorDB).filter(SensorDB.id_sensor == id_sensor).first()

