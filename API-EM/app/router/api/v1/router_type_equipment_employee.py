from app.database.TypeEquipmentEmployee import (get_all_type_equipment_employee, get_type_equipment_employee_by_id,
                                                get_type_equipment_by_employee_number, get_employee_by_type_equipment_id,
                                             post_type_equipment_employee, delete_type_equipment_employee,
                                                TypeEquipmentEmployeeView, TypeEquipmentEmployeeInDB)
from app.database.connection import get_db
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from typing import List
from app.database.TypeEquipment import TypeEquipmentView, TypeEquipmentInDB, get_type_equipment_by_id
from app.database.Employee import EmployeeView, EmployeeInDB, get_employee_by_id


router = APIRouter(
    prefix='/api/v1/type-equipment-employee',
    tags=['Type Equipment Employee'],
    responses={404: {"description": "Not found"}}
)


@router.get('', response_model=List[TypeEquipmentEmployeeView])
def get_all_type_equipment_employee_view(db=Depends(get_db)) -> List[TypeEquipmentEmployeeInDB]:
    return get_all_type_equipment_employee(db)


@router.get('/{employee_number}/type-equipments', response_model=List[TypeEquipmentView])
def get_type_equipment_by_employee_number_view(employee_number: str, db=Depends(get_db)) -> List[TypeEquipmentInDB]:
    type_equipment_employee = get_type_equipment_by_employee_number(db, employee_number)
    if type_equipment_employee is None:
        raise HTTPException(status_code=404, detail="Type equipment employee not found")
    type_equipment = [data[1] for data in type_equipment_employee]
    return type_equipment


@router.get('/{id_type_equipment}/employees', response_model=List[EmployeeView])
def get_employee_by_type_equipment_id_view(id_type_equipment: int, db=Depends(get_db)) -> List[EmployeeInDB]:
    type_equipment_employee = get_employee_by_type_equipment_id(db, id_type_equipment)
    if type_equipment_employee is None:
        raise HTTPException(status_code=404, detail="Type equipment employee not found")
    employees = [data[2] for data in type_equipment_employee]
    return employees


@router.post('', response_model=TypeEquipmentEmployeeView)
def post_type_equipment_employee_view(type_equipment_employee: TypeEquipmentEmployeeInDB,
                                      db=Depends(get_db)) -> TypeEquipmentEmployeeView:
    if get_type_equipment_by_id(db, type_equipment_employee.id_type_equipment) is None:
        raise HTTPException(status_code=404, detail="Type equipment not found")
    if get_employee_by_id(db, type_equipment_employee.employee_number) is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    if get_type_equipment_employee_by_id(db, type_equipment_employee.id_type_equipment,
                                         type_equipment_employee.employee_number) is not None:
        raise HTTPException(status_code=409, detail="Type equipment employee already exist")
    new_type_equipment_employee = TypeEquipmentEmployeeInDB(**type_equipment_employee.model_dump(exclude_unset=True))
    db_type_equipment_employee = post_type_equipment_employee(db, new_type_equipment_employee)
    return db_type_equipment_employee


@router.delete('/{employee_number}/{id_type_equipment_employee}/', response_model=TypeEquipmentEmployeeView)
def delete_type_equipment_employee_view(employee_number: str, id_type_equipment_employee: int,
                                        db=Depends(get_db)) -> bool:
    type_equipment_employee = get_type_equipment_employee_by_id(db, id_type_equipment_employee, employee_number)
    if type_equipment_employee is None:
        raise HTTPException(status_code=404, detail="Type equipment employee not found")
    delete_type_equipment_employee(db, id_type_equipment_employee, employee_number)
    return type_equipment_employee