from pydantic import BaseModel
from app.database.connection import Base, engine
from sqlalchemy import Column, Integer, ForeignKey
from typing import Optional
from app.database.DataBaseFunction import DataBaseRequest
from app.database.Sensor import SensorDB
from app.database.SensorHisto import SensorHistoDB


class IncidentSensorHistoDB(Base):
    # Table IncidentSensorHisto
    __tablename__ = 'incident_sensor_histo'
    id_incident = Column(Integer, ForeignKey('incident.id_incident', ondelete="cascade"), primary_key=True)
    id_sensor_histo = Column(Integer, ForeignKey('sensor_histo.id_sensor_histo', ondelete="cascade"), primary_key=True)


Base.metadata.create_all(bind=engine)


class IncidentSensorHistoView(BaseModel):
    id_incident: int
    id_sensor_histo: int




class IncidentSensorHistoUpdate(IncidentSensorHistoView):
    id_incident: Optional[int] = None
    id_sensor_histo: Optional[int] = None


class IncidentSensorHistoInDB(IncidentSensorHistoView):
    ...


def get_all_incident_sensor_histo(db):
    return DataBaseRequest.get_all_data(db, IncidentSensorHistoDB)


def get_incident_sensor_histo_by_id(db, id_incident: int, id_sensor_histo: int):
    data = (db.query(IncidentSensorHistoDB).
            filter(IncidentSensorHistoDB.id_incident == id_incident).
            filter(IncidentSensorHistoDB.id_sensor_histo == id_sensor_histo).first())
    return data


def get_incident_sensor_histo_by_incident_id(db, id_incident: int):
    return DataBaseRequest.get_all_data_by_something(db, IncidentSensorHistoDB,
                                                     IncidentSensorHistoDB.id_incident == id_incident)


def get_incident_sensor_histo_by_sensor_histo_id(db, id_sensor_histo: int):
    return DataBaseRequest.get_all_data_by_something(db, IncidentSensorHistoDB,
                                                     IncidentSensorHistoDB.id_sensor_histo == id_sensor_histo)


def get_incident_sensor_histo_by_sensor_id(db, id_sensor: int):
    data = (db.query(IncidentSensorHistoDB, SensorHistoDB, SensorDB).
            filter(IncidentSensorHistoDB.id_sensor_histo == SensorHistoDB.id_sensor_histo).
            filter(SensorHistoDB.id_sensor == SensorDB.id_sensor).filter(SensorDB.id_sensor == id_sensor).all())

    return data


def post_incident_sensor_histo(db, incident_sensor_histo: IncidentSensorHistoView):
    db_incident_sensor_histo = IncidentSensorHistoDB(**incident_sensor_histo.model_dump(exclude_unset=True))
    return DataBaseRequest.post_data(db, db_incident_sensor_histo)


def delete_incident_sensor_histo(db, id_incident: int, id_sensor_histo: int):
    DataBaseRequest.delete_data(db, IncidentSensorHistoDB,
                                IncidentSensorHistoDB.id_incident == id_incident and
                                IncidentSensorHistoDB.id_sensor_histo == id_sensor_histo)
    return True


