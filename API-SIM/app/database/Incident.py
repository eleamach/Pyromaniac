from pydantic import BaseModel
from app.database.connexion import Base, engine

from typing import Optional
from sqlalchemy import Column, Integer, Boolean


class IncidentDB(Base):
    # Table Incident
    __tablename__ = 'incident'
    incident_id = Column(Integer, primary_key=True, index=True, unique=True)
    incident_status = Column(Boolean)


Base.metadata.create_all(bind=engine)


class IncidentBase(BaseModel):
    incident_id: int
    incident_status: bool


class IncidentCreate(IncidentBase):
    incident_id: Optional[int] = None
    incident_status: Optional[bool] = False


class IncidentUpdate(IncidentCreate):
    incident_id: Optional[int] = None
    incident_status: Optional[bool] = None


class IncidentView(IncidentBase):
    ...


def get_all_incidents(db):
    return db.query(IncidentDB).all()


def get_incident_by_id(db, incident_id: int):
    return db.query(IncidentDB).filter(IncidentDB.incident_id == incident_id).first()


def post_incident(db, incident: IncidentCreate):

    db_incident = IncidentDB(**incident.model_dump(exclude_unset=True))
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident


def delete_incident(db, incident_id: int):
    db.query(IncidentDB).filter(IncidentDB.incident_id == incident_id).delete()
    db.commit()
    return {"message": "Incident deleted successfully."}


def patch_incident(db, incident_id: int, incident: IncidentUpdate):
    db_incident = db.query(IncidentDB).filter(IncidentDB.incident_id == incident_id).first()
    for var, value in vars(incident).items():
        if value is not None:
            setattr(db_incident, var, value)
    db.commit()
    db.refresh(db_incident)
    return db_incident

