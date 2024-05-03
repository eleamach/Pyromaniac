from pydantic import BaseModel
from app.database.connection import Base, engine
from sqlalchemy import Column, Float, String, Integer, DateTime, Boolean, ForeignKey
from typing import Optional, List
from app.database.DataBaseFunction import DataBaseRequest
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict


class TypeEquipmentDB(Base):
    # Table TypeEquipment
    __tablename__ = 'type_equipment'
    id_type_equipment = Column(Integer, primary_key=True, index=True)
    type_equipment_name = Column(String(50), unique=True)
    type_equipment_capacity_pers = Column(Integer)
    type_equipment_level_incident = Column(Integer)
    type_equipment_image = Column(String(250))


Base.metadata.create_all(bind=engine)


class TypeEquipmentView(BaseModel):
    id_type_equipment: Optional[int] = None
    type_equipment_name: str
    type_equipment_capacity_pers: int
    type_equipment_level_incident: int
    type_equipment_image: Optional[str] = None


class TypeEquipmentUpdate(TypeEquipmentView):
    type_equipment_name: Optional[str] = None
    type_equipment_capacity_pers: Optional[int] = None
    type_equipment_level_incident: Optional[int] = None
    type_equipment_image: Optional[str] = None


class TypeEquipmentInDB(TypeEquipmentView):
    ...



def get_all_type_equipment(db):
    return DataBaseRequest.get_all_data(db, TypeEquipmentDB)


def get_type_equipment_by_id(db, id_type_equipment: int):
    return DataBaseRequest.get_data_by_something(db, TypeEquipmentDB, TypeEquipmentDB.id_type_equipment == id_type_equipment)


def get_type_equipment_by_name(db, type_equipment_name: str):
    return DataBaseRequest.get_data_by_something(db, TypeEquipmentDB, TypeEquipmentDB.type_equipment_name == type_equipment_name)


def post_type_equipment(db, type_equipment: TypeEquipmentView):
    db_type_equipment = TypeEquipmentDB(**type_equipment.model_dump(exclude_unset=True))
    return DataBaseRequest.post_data(db, db_type_equipment)


def delete_type_equipment(db, id_type_equipment: int):
    DataBaseRequest.delete_data(db, TypeEquipmentDB, TypeEquipmentDB.id_type_equipment == id_type_equipment)
    return True


def update_type_equipment(db, id_type_equipment, type_equipment: TypeEquipmentView):
    db.query(TypeEquipmentDB).filter(TypeEquipmentDB.id_type_equipment == id_type_equipment).update(type_equipment.model_dump(exclude_unset=True))
    db.commit()
    return get_type_equipment_by_id(db, id_type_equipment)

