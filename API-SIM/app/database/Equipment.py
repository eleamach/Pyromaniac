from pydantic import BaseModel
from app.database.connexion import Base, engine

from typing import Optional
from sqlalchemy import Column, Integer, String, Float


class EquipmentDB(Base):
    # Table Equipment
    __tablename__ = 'equipment'
    equipment_id = Column(Integer, primary_key=True, index=True, unique=True)
    equipment_name = Column(String, unique=True)
    equipment_type_id = Column(Integer)
    equipment_longitude = Column(Float)
    equipment_latitude = Column(Float)


Base.metadata.create_all(bind=engine)


class EquipmentBase(BaseModel):
    equipment_id: int
    equipment_name: str
    equipment_type_id: int
    equipment_longitude: float
    equipment_latitude: float


class EquipmentCreate(EquipmentBase):
    equipment_id: Optional[int] = None
    equipment_name: str
    equipment_type_id: Optional[int] = None
    equipment_longitude: Optional[float] = None
    equipment_latitude: Optional[float] = None


class EquipmentUpdate(EquipmentBase):
    equipment_id: Optional[int] = None
    equipment_name: Optional[str] = None
    equipment_type_id: Optional[int] = None
    equipment_longitude: Optional[float] = None
    equipment_latitude: Optional[float] = None


class EquipmentView(EquipmentBase):
    ...


def get_all_equipments(db):
    return db.query(EquipmentDB).all()


def get_equipment_by_id(db, equipment_id: int):
    return db.query(EquipmentDB).filter(EquipmentDB.equipment_id == equipment_id).first()


def get_equipment_by_name(db, equipment_name: str):
    return db.query(EquipmentDB).filter(EquipmentDB.equipment_name == equipment_name).first()


def post_equipment(db, equipment: EquipmentCreate):
    db_equipment = EquipmentDB(**equipment.model_dump(exclude_unset=True))
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment


def delete_equipment(db, equipment_id: int):
    db.query(EquipmentDB).filter(EquipmentDB.equipment_id == equipment_id).delete()
    db.commit()
    return {"message": "Equipment deleted successfully"}


def patch_equipment(db, equipment_id: int, equipment: EquipmentUpdate):
    db_equipment = db.query(EquipmentDB).filter(EquipmentDB.equipment_id == equipment_id).first()
    for var, value in vars(equipment).items():
        if value is not None:
            setattr(db_equipment, var, value)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment



