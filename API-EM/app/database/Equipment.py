from pydantic import BaseModel
from app.database.connection import Base, engine
from sqlalchemy import Column, Float, String, Integer, DateTime, Boolean, ForeignKey
from typing import Optional, List
from app.database.DataBaseFunction import DataBaseRequest
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict


class EquipmentDB(Base):
    # Table Equipment
    __tablename__ = 'equipment'
    id_equipment = Column(Integer, primary_key=True, index=True)
    equipment_name = Column(String(50), unique=True)
    id_type_equipment = Column(Integer, ForeignKey('type_equipment.id_type_equipment', ondelete="cascade"))
    id_fire_station = Column(Integer, ForeignKey('firestation.id_fire_station', ondelete="cascade"))
    equipment_available = Column(Boolean, default=True)
    equipment_longitude = Column(Float)
    equipment_latitude = Column(Float)


Base.metadata.create_all(bind=engine)


class EquipmentView(BaseModel):
    equipment_name: str
    id_type_equipment: int
    id_fire_station: int
    equipment_available: Optional[bool] = None
    equipment_longitude: Optional[float] = None
    equipment_latitude: Optional[float] = None


class EquipmentUpdate(EquipmentView):
    equipment_name: Optional[str] = None
    id_type_equipment: Optional[int] = None
    id_fire_station: Optional[int] = None


class EquipmentInDB(EquipmentView):
    id_equipment: Optional[int] = None





def get_all_equipment(db):
    return DataBaseRequest.get_all_data(db, EquipmentDB)


def get_equipment_by_id(db, id_equipment: int):
    return DataBaseRequest.get_data_by_something(db, EquipmentDB, EquipmentDB.id_equipment == id_equipment)


def get_equipment_by_name(db, equipment_name: str):
    return DataBaseRequest.get_data_by_something(db, EquipmentDB, EquipmentDB.equipment_name == equipment_name)


def get_equipment_by_type_equipment_id(db, id_type_equipment: int):
    return DataBaseRequest.get_all_data_by_something(db, EquipmentDB, EquipmentDB.id_type_equipment == id_type_equipment)


def get_equipment_by_fire_station_id(db, id_fire_station: int):
    return DataBaseRequest.get_all_data_by_something(db, EquipmentDB, EquipmentDB.id_fire_station == id_fire_station)


def get_equipment_by_available(db, equipment_available: bool):
    return DataBaseRequest.get_all_data_by_something(db, EquipmentDB, EquipmentDB.equipment_available == equipment_available)


def post_equipment(db, equipment: EquipmentView):
    db_equipment = EquipmentDB(**equipment.model_dump(exclude_unset=True))
    return DataBaseRequest.post_data(db, db_equipment)


def delete_equipment(db, id_equipment: int):
    DataBaseRequest.delete_data(db, EquipmentDB, EquipmentDB.id_equipment == id_equipment)
    return True


def update_equipment(db, id_equipment, equipment: EquipmentView):
    db.query(EquipmentDB).filter(EquipmentDB.id_equipment == id_equipment).update(equipment.model_dump(exclude_unset=True))
    db.commit()
    return get_equipment_by_id(db, id_equipment)

