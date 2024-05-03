from pydantic import BaseModel
from app.database.connection import Base, engine
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from datetime import datetime


class EventIncidentTeamEquipmentDB(Base):
    # Table EventIncidentTeamEquipment
    __tablename__ = 'event_incident_team_equipment'
    id_event_incident_team_equipment = Column(Integer, primary_key=True, index=True, unique=True)
    id_incident_team_equipment = Column(Integer, ForeignKey('incident_team_equipment.id_incident_team_equipment', ondelete="cascade"))
    event_incident_team_equipment_longitude = Column(Float)
    event_incident_team_equipment_latitude = Column(Float)
    event_incident_team_equipment_date = Column(DateTime)
    event_incident_team_equipment_info = Column(String)


Base.metadata.create_all(bind=engine)


class EventIncidentTeamEquipmentBase(BaseModel):
    id_event_incident_team_equipment: int
    id_incident_team_equipment: int
    event_incident_team_equipment_longitude: float
    event_incident_team_equipment_latitude: float
    event_incident_team_equipment_date: datetime
    event_incident_team_equipment_info: str


class EventIncidentTeamEquipmentCreate(EventIncidentTeamEquipmentBase):
    id_event_incident_team_equipment: Optional[int] = None
    id_incident_team_equipment: int
    event_incident_team_equipment_longitude: Optional[float] = None
    event_incident_team_equipment_latitude: Optional[float] = None
    event_incident_team_equipment_date: Optional[datetime] = None
    event_incident_team_equipment_info: str


class EventIncidentTeamEquipmentUpdate(EventIncidentTeamEquipmentBase):
    id_event_incident_team_equipment: Optional[int] = None
    id_incident_team_equipment: Optional[int] = None
    event_incident_team_equipment_longitude: Optional[float] = None
    event_incident_team_equipment_latitude: Optional[float] = None
    event_incident_team_equipment_date: Optional[datetime] = None
    event_incident_team_equipment_info: Optional[str] = None


class EventIncidentTeamEquipmentView(EventIncidentTeamEquipmentBase):
    ...


def get_all_event_incident_team_equipments(db):
    return db.query(EventIncidentTeamEquipmentDB).all()


def get_event_incident_team_equipment_by_id(db, id_event_incident_team_equipment: int):
    return db.query(EventIncidentTeamEquipmentDB).filter(EventIncidentTeamEquipmentDB.id_event_incident_team_equipment == id_event_incident_team_equipment).first()


def get_event_incident_team_equipment_by_incident_team_equipment_id(db, id_incident_team_equipment: int):
    return db.query(EventIncidentTeamEquipmentDB).filter(EventIncidentTeamEquipmentDB.id_incident_team_equipment == id_incident_team_equipment).all()


def get_event_incident_team_equipment_by_coordinates(db, event_incident_team_equipment_longitude: float, event_incident_team_equipment_latitude: float):
    return db.query(EventIncidentTeamEquipmentDB).filter(EventIncidentTeamEquipmentDB.event_incident_team_equipment_longitude == event_incident_team_equipment_longitude,
                                                         EventIncidentTeamEquipmentDB.event_incident_team_equipment_latitude == event_incident_team_equipment_latitude).all()


def post_event_incident_team_equipment(db, event_incident_team_equipment: EventIncidentTeamEquipmentCreate):
    db_event_incident_team_equipment = EventIncidentTeamEquipmentDB(**event_incident_team_equipment.model_dump(exclude_unset=True))
    db.add(db_event_incident_team_equipment)
    db.commit()
    db.refresh(db_event_incident_team_equipment)
    return db_event_incident_team_equipment


def delete_event_incident_team_equipment(db, id_event_incident_team_equipment: int):
    db.query(EventIncidentTeamEquipmentDB).filter(EventIncidentTeamEquipmentDB.id_event_incident_team_equipment == id_event_incident_team_equipment).delete()
    db.commit()
    return {"message": "EventIncidentTeamEquipment deleted"}


def patch_event_incident_team_equipment(db, id_event_incident_team_equipment: int, event_incident_team_equipment: EventIncidentTeamEquipmentUpdate):
    db.query(EventIncidentTeamEquipmentDB).filter(EventIncidentTeamEquipmentDB.id_event_incident_team_equipment == id_event_incident_team_equipment).update(event_incident_team_equipment.model_dump(exclude_unset=True))
    db.commit()
    return get_event_incident_team_equipment_by_id(db, id_event_incident_team_equipment)