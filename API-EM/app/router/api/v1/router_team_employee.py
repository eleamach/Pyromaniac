from app.database.TeamEmployee import (get_all_team_employee, get_team_by_employee_number, get_team_employee_by_id,
                                       delete_team_employee, get_employee_by_team_id,
                                       get_employee_by_team_name, post_team_employee,
                                       TeamEmployeeInDB, TeamEmployeeView)
from app.database.connection import get_db
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from app.database.Employee import EmployeeView, get_employee_by_id
from app.database.Teams import TeamsView, get_team_by_id
from typing import List


router = APIRouter(
    prefix='/api/v1/team-employee',
    tags=['Team Employee'],
    responses={404: {"description": "Not found"}}
)


@router.get('', response_model=List[TeamEmployeeView])
def get_all_team_employee_view(db=Depends(get_db)) -> List[TeamEmployeeView]:
    return get_all_team_employee(db)


@router.get('/emp/{employee_number}/tea/{id_team_employee}', response_model=TeamEmployeeView)
def get_team_employee_by_id_view(employee_number: str, id_team_employee: int, db=Depends(get_db)) -> TeamEmployeeView:
    team_employee = get_team_employee_by_id(db, id_team_employee, employee_number)
    if team_employee is None:
        raise HTTPException(status_code=404, detail="Team employee not found")
    return team_employee


@router.get('/{team_name}/employees', response_model=List[EmployeeView])
def get_team_employee_by_name_view(team_name: str, db=Depends(get_db)) -> List[EmployeeView]:
    team_employee = get_employee_by_team_name(db, team_name)
    if team_employee is None:
        raise HTTPException(status_code=404, detail="Team employee not found")
    employees = [data[2] for data in team_employee]
    return employees


@router.get('/{id_team}/employees', response_model=List[EmployeeView])
def get_team_employee_by_id_view(id_team: int, db=Depends(get_db)) -> List[EmployeeView]:
    team_employee = get_employee_by_team_id(db, id_team)
    if team_employee is None:
        raise HTTPException(status_code=404, detail="Team employee not found")
    employees = [data[2] for data in team_employee]
    return employees

@router.get('/{employee_number}/teams', response_model=List[TeamsView])
def get_team_by_employee_number_view(employee_number: str, db=Depends(get_db)) -> List[TeamsView]:
    team_employee = get_team_by_employee_number(db, employee_number)
    if team_employee is None:
        raise HTTPException(status_code=404, detail="Team employee not found")
    teams = [data[1] for data in team_employee]
    return teams


@router.post('', response_model=TeamEmployeeView)
def post_team_employee_view(team_employee: TeamEmployeeInDB, db=Depends(get_db)) -> TeamEmployeeInDB:
    if get_team_by_id(db, team_employee.id_team) is None:
        raise HTTPException(status_code=404, detail="Team not found")
    if get_employee_by_id(db, team_employee.employee_number) is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    if get_team_employee_by_id(db, team_employee.id_team, team_employee.employee_number) is not None:
        raise HTTPException(status_code=409, detail="Team employee already exist")
    new_team_employee = TeamEmployeeView(**team_employee.model_dump(exclude_unset=True))
    db_team_employee = post_team_employee(db, new_team_employee)
    return db_team_employee


@router.delete('/emp/{employee_number}/tea/{id_team_employee}/', response_model=TeamEmployeeView)
def delete_team_employee_view(employee_number: str, id_team_employee: int, db=Depends(get_db)) -> bool:
    team_employee = get_team_employee_by_id(db, id_team_employee, employee_number)
    if team_employee is None:
        raise HTTPException(status_code=404, detail="Team employee not found")
    delete_team_employee(db, id_team_employee, employee_number)
    return team_employee