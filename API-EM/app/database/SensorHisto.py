from pydantic import BaseModel
from app.database.connection import Base, engine
from sqlalchemy import Column, Float, String, Integer, DateTime, Boolean, ForeignKey
from typing import Optional, List
from datetime import datetime
from app.database.DataBaseFunction import DataBaseRequest
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict


class SensorHistoDB(Base):
    # Table SensorHisto
    __tablename__ = 'sensor_histo'
    id_sensor_histo = Column(Integer, primary_key=True, index=True)
    id_sensor = Column(Integer, ForeignKey('sensor.id_sensor', ondelete="cascade"))
    sensor_histo_date = Column(DateTime)
    sensor_histo_value = Column(Float)
    sensor_histo_is_processed = Column(Boolean)




class SensorHistoView(BaseModel):
    id_sensor: int
    sensor_histo_date: datetime
    sensor_histo_value: float
    sensor_histo_is_processed: Optional[bool] = False


class SensorHistoUpdate(SensorHistoView):
    id_sensor: Optional[int] = None
    sensor_histo_date: Optional[datetime] = None
    sensor_histo_value: Optional[float] = None
    sensor_histo_is_processed: Optional[bool] = None


class SensorHistoInDB(SensorHistoView):
    id_sensor_histo: Optional[int] = None



def get_all_sensor_histo(db):
    return DataBaseRequest.get_all_data(db, SensorHistoDB)


def get_sensor_histo_by_id(db, id_sensor_histo: int):
    return DataBaseRequest.get_data_by_something(db, SensorHistoDB, SensorHistoDB.id_sensor_histo == id_sensor_histo)


def get_sensor_histo_by_sensor_id(db, id_sensor: int):
    return DataBaseRequest.get_all_data_by_something(db, SensorHistoDB, SensorHistoDB.id_sensor == id_sensor)


def get_all_non_processed_sensor_histo(db):
    return DataBaseRequest.get_all_data_by_something(db, SensorHistoDB, SensorHistoDB.sensor_histo_is_processed == False)


def get_all_non_processed_sensor_histo_by_sensor_id(db, id_sensor: int):
    data = (db.query(SensorHistoDB).
            filter(SensorHistoDB.sensor_histo_is_processed == False).
            filter(SensorHistoDB.id_sensor == id_sensor).all())
    return data

def post_sensor_histo(db, sensor_histo: SensorHistoView):
    db_sensor_histo = SensorHistoDB(**sensor_histo.model_dump(exclude_unset=True))
    return DataBaseRequest.post_data(db, db_sensor_histo)


def delete_sensor_histo(db, id_sensor_histo: int):
    DataBaseRequest.delete_data(db, SensorHistoDB, SensorHistoDB.id_sensor_histo == id_sensor_histo)
    return True


def update_sensor_histo(db, id_sensor_histo, sensor_histo: SensorHistoView):
    db.query(SensorHistoDB).filter(SensorHistoDB.id_sensor_histo == id_sensor_histo).update(sensor_histo.model_dump(exclude_unset=True))
    db.commit()
    return get_sensor_histo_by_id(db, id_sensor_histo)