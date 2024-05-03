from pydantic import BaseModel
from app.database.connexion import Base, engine
from sqlalchemy.orm import relationship, backref
from typing import Optional
from sqlalchemy import Column, Integer, Float, DateTime, Boolean, ForeignKey
from app.database.Incident import IncidentView
from app.database.Equipment import EquipmentView
from app.database.EquipmentEvent import EquipmentEventView


class IncidentEquipmentDB(Base):
    # Table IncidentEquipment
    __tablename__ = 'incident_equipment'
    incident_id = Column(Integer, ForeignKey('incident.incident_id'), primary_key=True)
    incident = relationship("IncidentDB", backref=backref("incident_equipment", cascade="all, delete-orphan"))
    equipment_id = Column(Integer, ForeignKey('equipment.equipment_id'), primary_key=True)
    equipment = relationship("EquipmentDB", backref=backref("incident_equipment", cascade="all, delete-orphan"))
    equipment_event_id = Column(Integer, ForeignKey('equipment_event.equipment_event_id'), primary_key=True)
    equipment_event = relationship("EquipmentEventDB", backref=backref("incident_equipment", cascade="all, delete-orphan"))


Base.metadata.create_all(bind=engine)


class IncidentEquipmentBase(BaseModel):
    incident_id: int
    equipment_id: int
    equipment_event_id: int


class IncidentEquipmentCreate(IncidentEquipmentBase):
    incident_id: int
    equipment_id: int
    equipment_event_id: int


class IncidentEquipmentView(BaseModel):
    incident: Optional[IncidentView] = []
    equipment: Optional[EquipmentView] = []
    equipment_event: Optional[EquipmentEventView] = []


def get_all_incident_equipments(db):
    return db.query(IncidentEquipmentDB).all()


def get_incident_equipment_by_id(db, incident_id: int, equipment_id: int, equipment_event_id: int):
    return db.query(IncidentEquipmentDB).filter(IncidentEquipmentDB.incident_id == incident_id).filter(IncidentEquipmentDB.equipment_id == equipment_id).filter(IncidentEquipmentDB.equipment_event_id == equipment_event_id).first()


def get_incident_equipment_by_incident_id(db, incident_id: int):
    return db.query(IncidentEquipmentDB).filter(IncidentEquipmentDB.incident_id == incident_id).all()


def get_incident_equipment_by_equipment_id(db, equipment_id: int):
    return db.query(IncidentEquipmentDB).filter(IncidentEquipmentDB.equipment_id == equipment_id).all()


def get_incident_equipment_by_equipment_event_id(db, equipment_event_id: int):
    return db.query(IncidentEquipmentDB).filter(IncidentEquipmentDB.equipment_event_id == equipment_event_id).all()


def post_incident_equipment(db, incident_equipment: IncidentEquipmentCreate):
    db_incident_equipment = IncidentEquipmentDB(**incident_equipment.model_dump(exclude_unset=True))
    db.add(db_incident_equipment)
    db.commit()
    db.refresh(db_incident_equipment)
    return db_incident_equipment


def delete_incident_equipment(db, incident_id: int, equipment_id: int, equipment_event_id: int):
    db.query(IncidentEquipmentDB).filter(IncidentEquipmentDB.incident_id == incident_id).filter(IncidentEquipmentDB.equipment_id == equipment_id).filter(IncidentEquipmentDB.equipment_event_id == equipment_event_id).delete()
    db.commit()
    return {"message": "IncidentEquipment deleted"}


