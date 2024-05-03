from pydantic import BaseModel
from app.database.connexion import Base, engine

from typing import Optional
from sqlalchemy import Column, Integer, Float, DateTime, Boolean, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship, backref

from app.database import Sensor



class SensorHistoDB(Base):
    # Table SensorHisto
    __tablename__ = 'sensor_histo'
    sensor_histo_id = Column(Integer, primary_key=True, index=True, unique=True)
    sensor_histo_date = Column(DateTime)
    sensor_histo_value = Column(Float)
    sensor_histo_is_processed = Column(Boolean)
    sensor_id = Column(Integer, ForeignKey('sensor.sensor_id'))
    sensor = relationship("SensorDB", backref=backref("sensor_histo", cascade="all, delete-orphan"))




Base.metadata.create_all(bind=engine)


class SensorHistoBase(BaseModel):
    sensor_histo_id: int
    sensor_histo_date: datetime
    sensor_histo_value: float
    sensor_histo_is_processed: bool
    sensor_id: int


class SensorHistoCreate(SensorHistoBase):
    sensor_histo_id: Optional[int] = None
    sensor_histo_date: datetime
    sensor_histo_value: float
    sensor_histo_is_processed: Optional[bool] = False
    sensor_id: int


class SensorHistoUpdate(SensorHistoBase):
    sensor_histo_id: Optional[int] = None
    sensor_histo_date: Optional[datetime] = None
    sensor_histo_value: Optional[float] = None
    sensor_histo_is_processed: Optional[bool] = None
    sensor_id: Optional[int] = None


class SensorHistoView(SensorHistoBase):
    sensor: Sensor.SensorView = None



def get_all_sensor_histos(db):
    return db.query(SensorHistoDB).all()


def get_sensor_histo_by_id(db, sensor_histo_id: int):
    return db.query(SensorHistoDB).filter(SensorHistoDB.sensor_histo_id == sensor_histo_id).first()


def get_sensor_histo_by_sensor_id(db, sensor_id: int):
    return db.query(SensorHistoDB).filter(SensorHistoDB.sensor_id == sensor_id).all()


def post_sensor_histo(db, sensor_histo: SensorHistoCreate):
    db_sensor_histo = SensorHistoDB(**sensor_histo.model_dump(exclude_unset=True))
    db.add(db_sensor_histo)
    db.commit()
    db.refresh(db_sensor_histo)
    return db_sensor_histo


def delete_sensor_histo(db, sensor_histo_id: int):
    db.query(SensorHistoDB).filter(SensorHistoDB.sensor_histo_id == sensor_histo_id).delete()
    db.commit()
    return {"message": "SensorHisto deleted successfully."}


def patch_sensor_histo(db, sensor_histo_id: int, sensor_histo: SensorHistoUpdate):
    db_sensor_histo = db.query(SensorHistoDB).filter(SensorHistoDB.sensor_histo_id == sensor_histo_id).first()
    for var, value in vars(sensor_histo).items():
        if value is not None:
            setattr(db_sensor_histo, var, value)
    db.commit()
    db.refresh(db_sensor_histo)
    return db_sensor_histo

