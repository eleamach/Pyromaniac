from app.database.connexion import Base, engine
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float


class SensorEventDB(Base):

    # Table SensorEvent
    __tablename__ = 'sensor_event'
    id_sensor_event = Column(Integer, primary_key=True, index=True, unique=True)
    event_name = Column(String, unique=True)
    event_pound = Column(Float)


Base.metadata.create_all(bind=engine)


class SensorEventBase(BaseModel):
    id_sensor_event: int
    event_name: str
    event_pound: float


class SensorEventCreate(SensorEventBase):
    id_sensor_event: Optional[int] = None
    event_name: str
    event_pound: float


class SensorEventUpdate(SensorEventBase):
    id_sensor_event: Optional[int] = None
    event_name: Optional[str] = None
    event_pound: Optional[float] = None


class SensorEventView(SensorEventBase):
    ...


def get_all_sensor_events(db):
    return db.query(SensorEventDB).all()


def get_sensor_event_by_id(db, id_sensor_event: int):
    return db.query(SensorEventDB).filter(SensorEventDB.id_sensor_event == id_sensor_event).first()


def get_sensor_event_by_name(db, event_name: str):
    return db.query(SensorEventDB).filter(SensorEventDB.event_name == event_name).first()


def post_sensor_event(db, sensor_event: SensorEventCreate):
    db_sensor_event = SensorEventDB(**sensor_event.model_dump(exclude_unset=True))

    db.add(db_sensor_event)
    db.commit()
    db.refresh(db_sensor_event)
    return db_sensor_event


def delete_sensor_event(db, id_sensor_event: int):
    db.query(SensorEventDB).filter(SensorEventDB.id_sensor_event == id_sensor_event).delete()

    db.commit()
    return {"message": "SensorEvent deleted successfully."}


def patch_sensor_event(db, id_sensor_event: int, sensor_event: SensorEventUpdate):
    db_sensor_event = db.query(SensorEventDB).filter(SensorEventDB.id_sensor_event == id_sensor_event).first()

    for var, value in vars(sensor_event).items():
        if value is not None:
            setattr(db_sensor_event, var, value)
    db.commit()
    db.refresh(db_sensor_event)
    return db_sensor_event


