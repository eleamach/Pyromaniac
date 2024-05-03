from pydantic import BaseModel
from app.database.connexion import Base, engine
from app.database.SensorHisto import SensorHistoView
from app.database.SensorEvent import SensorEventView
from app.database.Incident import IncidentView

from typing import Optional
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref



class IncidentSensorHistoDB(Base):
    # Table Incident
    __tablename__ = 'incident_sensor_histo'
    incident_id = Column(ForeignKey('incident.incident_id'), primary_key=True)
    incident = relationship("IncidentDB", backref=backref("incident_sensor_histo", cascade="all, delete-orphan"))
    sensor_histo_id = Column(ForeignKey('sensor_histo.sensor_histo_id'), primary_key=True)
    sensor_histo = relationship("SensorHistoDB", backref=backref("incident_sensor_histo", cascade="all, delete-orphan"))
    sensor_event_id = Column(ForeignKey('sensor_event.id_sensor_event'), primary_key=True)
    sensor_event = relationship("SensorEventDB", backref=backref("incident_sensor_histo", cascade="all, delete-orphan"))



Base.metadata.create_all(bind=engine)


class IncidentSensorHistoBase(BaseModel):
    incident_id: int
    sensor_histo_id: int
    event_id: int


class IncidentSensorHistoCreate(IncidentSensorHistoBase):
    incident_id: Optional[int] = None
    sensor_histo_id: int
    event_id: int


class IncidentSensorHistoUpdate(IncidentSensorHistoBase):
    incident_id: Optional[int] = None
    sensor_histo_id: Optional[int] = None
    event_id: Optional[int] = None


class IncidentSensorHistoView(BaseModel):
    sensor_histo: SensorHistoView = []
    sensor_event: SensorEventView = []
    incident: IncidentView = []



def get_all_incident_sensor_histo(db):
    return db.query(IncidentSensorHistoDB).all()


def get_incident_sensor_histo_by_pk(db, incident_id: int, sensor_histo_id: int, event_id: int):
    return (db.query(IncidentSensorHistoDB).
            filter(IncidentSensorHistoDB.incident_id == incident_id).
            filter(IncidentSensorHistoDB.sensor_histo_id == sensor_histo_id).
            filter(IncidentSensorHistoDB.event_id == event_id).first())


def get_incident_sensor_histo_by_incident_id(db, incident_id: int):
    return db.query(IncidentSensorHistoDB).filter(IncidentSensorHistoDB.incident_id == incident_id).all()


def get_incident_sensor_histo_by_sensor_histo_id(db, sensor_histo_id: int):
    return db.query(IncidentSensorHistoDB).filter(IncidentSensorHistoDB.sensor_histo_id == sensor_histo_id).all()


def get_incident_sensor_histo_by_event_id(db, event_id: int):
    return db.query(IncidentSensorHistoDB).filter(IncidentSensorHistoDB.event_id == event_id).all()


def post_incident_sensor_histo(db, incident_sensor_histo: IncidentSensorHistoCreate):
    db_incident_sensor_histo = IncidentSensorHistoDB(**incident_sensor_histo.model_dump(exclude_unset=True))
    db.add(db_incident_sensor_histo)
    db.commit()
    db.refresh(db_incident_sensor_histo)
    return db_incident_sensor_histo


def delete_incident_sensor_histo(db, incident_id: int, sensor_histo_id: int, event_id: int):
    db.query(IncidentSensorHistoDB).filter(IncidentSensorHistoDB.incident_id == incident_id).\
        filter(IncidentSensorHistoDB.sensor_histo_id == sensor_histo_id).\
        filter(IncidentSensorHistoDB.event_id == event_id).delete()
    db.commit()
    return {"message": "IncidentSensorHisto deleted successfully."}


def patch_incident_sensor_histo(db, incident_id: int, sensor_histo_id: int, event_id: int,
                                incident_sensor_histo: IncidentSensorHistoUpdate):
    db_incident_sensor_histo = (db.query(IncidentSensorHistoDB).
                                filter(IncidentSensorHistoDB.incident_id == incident_id).
                                filter(IncidentSensorHistoDB.sensor_histo_id == sensor_histo_id).
                                filter(IncidentSensorHistoDB.event_id == event_id).first())
    for var, value in vars(incident_sensor_histo).items():
        if value is not None:
            setattr(db_incident_sensor_histo, var, value)
    db.commit()
    db.refresh(db_incident_sensor_histo)
    return db_incident_sensor_histo

