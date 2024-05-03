from pydantic import BaseModel
from app.database.connexion import Base, engine

from typing import Optional
from sqlalchemy import Column, Integer, Float, String
from datetime import datetime


class EquipmentEventDB(Base):
    # Table EquipmentEvent
    __tablename__ = 'equipment_event'
    equipment_event_id = Column(Integer, primary_key=True, index=True, unique=True)
    event_name = Column(String, unique=True)
    event_pound = Column(Float)


Base.metadata.create_all(bind=engine)


class EquipmentEventBase(BaseModel):
    equipment_event_id: int
    event_name: str
    event_pound: float


class EquipmentEventCreate(EquipmentEventBase):
    equipment_event_id: Optional[int] = None
    event_name: str
    event_pound: float


class EquipmentEventUpdate(EquipmentEventBase):
    equipment_event_id: Optional[int] = None
    event_name: Optional[str] = None
    event_pound: Optional[float] = None


class EquipmentEventView(EquipmentEventBase):
    ...


def get_all_equipment_events(db):
    return db.query(EquipmentEventDB).all()


def get_equipment_event_by_id(db, equipment_event_id: int):
    return db.query(EquipmentEventDB).filter(EquipmentEventDB.equipment_event_id == equipment_event_id).first()


def get_equipment_event_by_name(db, event_name: str):
    return db.query(EquipmentEventDB).filter(EquipmentEventDB.event_name == event_name).first()


def post_equipment_event(db, equipment_event: EquipmentEventCreate):
    db_equipment_event = EquipmentEventDB(**equipment_event.model_dump(exclude_unset=True))
    db.add(db_equipment_event)
    db.commit()
    db.refresh(db_equipment_event)
    return db_equipment_event


def delete_equipment_event(db, equipment_event_id: int):
    db.query(EquipmentEventDB).filter(EquipmentEventDB.equipment_event_id == equipment_event_id).delete()
    db.commit()
    return {'message': 'EquipmentEvent deleted'}


def patch_equipment_event(db, equipment_event_id: int, equipment_event: EquipmentEventUpdate):
    db_equipment_event = (db.query(EquipmentEventDB).filter(EquipmentEventDB.equipment_event_id == equipment_event_id)
                          .update(equipment_event.model_dump(exclude_unset=True)))
    db.commit()
    return db.query(EquipmentEventDB).filter(EquipmentEventDB.equipment_event_id == equipment_event_id).first()



