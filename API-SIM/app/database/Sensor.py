from pydantic import BaseModel
from app.database.connexion import Base, engine
from typing import Optional
from sqlalchemy import Column, Integer, Float



class SensorDB(Base):
    # Table Sensor
    __tablename__ = 'sensor'
    sensor_id = Column(Integer, primary_key=True, index=True, unique=True)
    sensor_longitude = Column(Float)
    sensor_latitude = Column(Float)



Base.metadata.create_all(bind=engine)


class SensorBase(BaseModel):
    sensor_id: int
    sensor_longitude: float
    sensor_latitude: float


class SensorCreate(SensorBase):
    sensor_id: Optional[int] = None
    sensor_longitude: Optional[float] = None
    sensor_latitude: Optional[float] = None


class SensorUpdate(SensorCreate):
    sensor_id: Optional[int] = None
    sensor_longitude: Optional[float] = None
    sensor_latitude: Optional[float] = None


class SensorView(SensorBase):
    ...


def get_all_sensors(db):
    return db.query(SensorDB).all()


def get_sensor_by_id(db, sensor_id: int):
    return db.query(SensorDB).filter(SensorDB.sensor_id == sensor_id).first()


def post_sensor(db, sensor: SensorCreate):
    db_sensor = SensorDB(**sensor.model_dump(exclude_unset=True))
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


def delete_sensor(db, sensor_id: int):
    db.query(SensorDB).filter(SensorDB.sensor_id == sensor_id).delete()
    db.commit()
    return {"message": "Sensor deleted successfully."}


def patch_sensor(db, sensor_id: int, sensor: SensorUpdate):
    db_sensor = db.query(SensorDB).filter(SensorDB.sensor_id == sensor_id).first()
    for var, value in vars(sensor).items():
        if value is not None:
            setattr(db_sensor, var, value)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor




