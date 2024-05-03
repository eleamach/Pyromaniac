from pydantic import BaseModel
from app.database.connection import Base, engine
from sqlalchemy import Column, Float, String, Integer, DateTime, Boolean, ForeignKey
from typing import Optional, List
from app.database.DataBaseFunction import DataBaseRequest
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict


class IncidentDB(Base):
    # Table Incident
    __tablename__ = 'incident'
    id_incident = Column(Integer, primary_key=True, index=True)
    incident_status = Column(Boolean)


Base.metadata.create_all(bind=engine)


class IncidentView(BaseModel):
    incident_status: Optional[bool] = False


class IncidentUpdate(IncidentView):
    incident_status: bool


class IncidentInDB(IncidentView):
    id_incident: Optional[int] = None


def get_all_incidents(db):
    return DataBaseRequest.get_all_data(db, IncidentDB)


def get_incident_by_id(db, id_incident: int):
    return DataBaseRequest.get_data_by_something(db, IncidentDB, IncidentDB.id_incident == id_incident)


def get_incident_by_status(db, incident_status: bool):
    return DataBaseRequest.get_all_data_by_something(db, IncidentDB, IncidentDB.incident_status == incident_status)


def post_incident(db, incident: IncidentView):
    db_incident = IncidentDB(**incident.model_dump(exclude_unset=True))
    return DataBaseRequest.post_data(db, db_incident)


def delete_incident(db, id_incident: int):
    DataBaseRequest.delete_data(db, IncidentDB, IncidentDB.id_incident == id_incident)
    return True


def update_incident(db, id_incident, incident: IncidentView):
    db.query(IncidentDB).filter(IncidentDB.id_incident == id_incident).update(incident.model_dump(exclude_unset=True))
    db.commit()
    return get_incident_by_id(db, id_incident)