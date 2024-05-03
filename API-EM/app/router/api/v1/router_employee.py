from app.database.Employee import get_all_employees, get_employee_by_id, post_employee, delete_employee, update_employee,EmployeeUpdate, EmployeeView, EmployeeInDB, EmployeeCreate
from app.database.connection import get_db
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from typing import List

router = APIRouter(
    prefix='/api/v1/employees',
    tags=['Employees'],
    responses={404: {"description": "Not found"}}
)


@router.get('', response_model=List[EmployeeView])
def get_all_employees_view(db=Depends(get_db)) -> List[EmployeeInDB]:
    return get_all_employees(db)


@router.get('/{employee_number}', response_model=EmployeeView)
def get_employee_by_id_view(employee_number: str, db=Depends(get_db)) -> EmployeeInDB:
    employee = get_employee_by_id(db, employee_number)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.post('', response_model=EmployeeView)
def post_employee_view(employee: EmployeeCreate, db=Depends(get_db)) -> EmployeeInDB:
    if get_employee_by_id(db, employee.employee_number) is not None:
        raise HTTPException(status_code=409, detail="Employee already exist")
    new_employee = EmployeeInDB(**employee.model_dump(exclude_unset=True))
    db_employee = post_employee(db, new_employee)
    return db_employee


@router.delete('/{employee_number}', response_model=EmployeeView)
def delete_employee_view(employee_number: str, db=Depends(get_db)) -> bool:
    employee = get_employee_by_id(db, employee_number)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    delete_employee(db, employee_number)
    return employee


@router.patch('/{employee_number}', response_model=EmployeeView)
def update_employee_view(employee_number: str, employee: EmployeeUpdate, db=Depends(get_db)) -> EmployeeView:
    test_employee = get_employee_by_id(db, employee_number)
    if test_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    db_employee = update_employee(db, employee_number, employee)
    return db_employee