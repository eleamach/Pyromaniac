from pydantic import BaseModel
from app.database.connection import Base, engine
from sqlalchemy import Column, Float, String, Integer, DateTime, Boolean
from typing import Optional, List
from app.internal.password import Hash
from app.database.DataBaseFunction import DataBaseRequest
import datetime


class EmployeeDB(Base):
    # Table Employe
    __tablename__ = 'employee'
    employee_number = Column(String(50),primary_key=True, index=True, unique=True)
    employee_first_name = Column(String(50))
    employee_last_name = Column(String(50))
    employee_password = Column(String(250), nullable=True)
    employee_token = Column(String(250))
    employee_disable = Column(Boolean)


Base.metadata.create_all(bind=engine)


class EmployeeBase(BaseModel):
    employee_first_name: str
    employee_last_name: str
    employee_number: str
    employee_disable: Optional[bool] = False


class EmployeeCreate(EmployeeBase):
    employee_password: Optional[str] = None


class EmployeeUpdate(EmployeeCreate):
    employee_first_name: Optional[str] = None
    employee_last_name: Optional[str] = None
    employee_disable: Optional[bool] = None
    employee_password: Optional[str] = None


class EmployeeView(EmployeeBase):
    ...


class EmployeeInDB(EmployeeView):
    employee_password: Optional[str] = None
    employee_token: Optional[str] = None



def get_all_employees(db):
    return DataBaseRequest.get_all_data(db, EmployeeDB)


def get_employee_by_id(db, employee_number: str):
    return DataBaseRequest.get_data_by_something(db, EmployeeDB, EmployeeDB.employee_number == employee_number)


def post_employee(db, employee: EmployeeCreate):
    db_employee = EmployeeDB(**employee.model_dump(exclude_unset=True))
    if employee.employee_password is not None:
        db_employee.employee_password = Hash.get_hashed_password(employee.employee_password)
        db_employee.employee_token = Hash.get_hashed_password(employee.employee_first_name+employee.employee_last_name+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def update_employee(db, employee_number: str, employee: EmployeeCreate):
    db_employee = (db.query(EmployeeDB).filter(EmployeeDB.employee_number == employee_number).
                   update(employee.model_dump(exclude_unset=True)))
    db.commit()
    return db.query(EmployeeDB).filter(EmployeeDB.employee_number == employee_number).first()


def delete_employee(db, employee_number: str):
    db.query(EmployeeDB).filter(EmployeeDB.employee_number == employee_number).delete()
    db.commit()
    return True