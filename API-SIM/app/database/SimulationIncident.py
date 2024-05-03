from app.database.Incident import IncidentView
from app.database.Simulation import SimulationView

from pydantic import BaseModel
from app.database.connexion import Base, engine

from typing import Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, backref



class SimulationIncidentDB(Base):
    # Table SimulationIncident
    __tablename__ = 'simulation_incident'
    simulation_id = Column(Integer, ForeignKey('simulation.simulation_id'), primary_key=True)
    simulation = relationship("SimulationDB", backref=backref("simulation_incident", cascade="all, delete-orphan"))
    incident_id = Column(Integer, ForeignKey('incident.incident_id'), primary_key=True)
    incident = relationship("IncidentDB", backref=backref("simulation_incident", cascade="all, delete-orphan"))



Base.metadata.create_all(bind=engine)


class SimulationIncidentBase(BaseModel):
    simulation_id: int
    incident_id: int


class SimulationIncidentCreate(SimulationIncidentBase):
    simulation_id: int
    incident_id: int


class SimulationIncidentViewID(SimulationIncidentBase):
    simulation_id: int
    incident_id: int


class SimulationIncidentView(BaseModel):
    simulation: Optional[SimulationView] = []
    incident: Optional[IncidentView] = []


def get_all_simulation_incidents(db):
    return db.query(SimulationIncidentDB).all()



def get_simulation_incident_by_id(db, simulation_id: int, incident_id: int):
    return (db.query(SimulationIncidentDB).
            filter(SimulationIncidentDB.simulation_id == simulation_id).
            filter(SimulationIncidentDB.incident_id == incident_id).first())


def get_simulation_incident_by_simulation_id(db, simulation_id: int):
    return db.query(SimulationIncidentDB).filter(SimulationIncidentDB.simulation_id == simulation_id).all()


def get_simulation_incident_by_incident_id(db, incident_id: int):
    return db.query(SimulationIncidentDB).filter(SimulationIncidentDB.incident_id == incident_id).all()


def post_simulation_incident(db, simulation_incident: SimulationIncidentCreate):
    db_simulation_incident = SimulationIncidentDB(**simulation_incident.model_dump(exclude_unset=True))
    db.add(db_simulation_incident)
    db.commit()
    db.refresh(db_simulation_incident)
    return db_simulation_incident


def delete_simulation_incident(db, simulation_id: int, incident_id: int):
    db.query(SimulationIncidentDB).filter(SimulationIncidentDB.simulation_id == simulation_id).filter(SimulationIncidentDB.incident_id == incident_id).delete()
    db.commit()
    return {"message": "SimulationIncident successfully deleted"}