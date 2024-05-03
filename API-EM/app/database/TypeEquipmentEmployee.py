from pydantic import BaseModel
from app.database.connection import Base, engine
from sqlalchemy import Column, Float, String, Integer, DateTime, Boolean, ForeignKey
from typing import Optional, List
from app.database.DataBaseFunction import DataBaseRequest
from app.database.TypeEquipment import TypeEquipmentDB
from app.database.Employee import EmployeeDB
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict


class TypeEquipmentEmployeeDB(Base):
    # Table Employe
    __tablename__ = 'type_equipment_employee'
    id_type_equipment = Column(Integer, ForeignKey('type_equipment.id_type_equipment', ondelete="cascade"), primary_key=True)
    employee_number = Column(String(50), ForeignKey('employee.employee_number', ondelete="cascade"), primary_key=True)

Base.metadata.create_all(bind=engine)


class TypeEquipmentEmployeeView(BaseModel):
    id_type_equipment: int
    employee_number: str


class TypeEquipmentEmployeeInDB(TypeEquipmentEmployeeView):
    ...



def get_all_type_equipment_employee(db):
    return DataBaseRequest.get_all_data(db, TypeEquipmentEmployeeDB)


def get_type_equipment_employee_by_id(db, id_type_equipment: int, employee_number: str):
    data = (db.query(TypeEquipmentEmployeeDB).
            filter(TypeEquipmentEmployeeDB.id_type_equipment == id_type_equipment).
            filter(TypeEquipmentEmployeeDB.employee_number == employee_number).first())
    return data


def get_type_equipment_by_employee_number(db, employee_number: str):
    data = (db.query(TypeEquipmentEmployeeDB, TypeEquipmentDB, EmployeeDB).
            filter(TypeEquipmentEmployeeDB.id_type_equipment == TypeEquipmentDB.id_type_equipment).
            filter(TypeEquipmentEmployeeDB.employee_number == EmployeeDB.employee_number).
            filter(EmployeeDB.employee_number == employee_number).all())
    return data


def get_employee_by_type_equipment_id(db, id_type_equipment: int):
    data = (db.query(TypeEquipmentEmployeeDB, TypeEquipmentDB, EmployeeDB).
            filter(TypeEquipmentEmployeeDB.id_type_equipment == TypeEquipmentDB.id_type_equipment).
            filter(TypeEquipmentEmployeeDB.employee_number == EmployeeDB.employee_number).
            filter(TypeEquipmentDB.id_type_equipment == id_type_equipment).all())

    return data


def post_type_equipment_employee(db, type_equipment_employee: TypeEquipmentEmployeeView):
    db_type_equipment_employee = TypeEquipmentEmployeeDB(**type_equipment_employee.model_dump(exclude_unset=True))
    return DataBaseRequest.post_data(db, db_type_equipment_employee)


def delete_type_equipment_employee(db, id_type_equipment: int, employee_number: str):
    db.query(TypeEquipmentEmployeeDB).filter(TypeEquipmentEmployeeDB.id_type_equipment == id_type_equipment).filter(TypeEquipmentEmployeeDB.employee_number == employee_number).delete()
    db.commit()
    return True