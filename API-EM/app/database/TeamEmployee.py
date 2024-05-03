from pydantic import BaseModel
from app.database.connection import Base, engine
from sqlalchemy import Column, Integer, ForeignKey, String
from app.database.DataBaseFunction import DataBaseRequest
from app.database.Teams import TeamsDB
from app.database.Employee import EmployeeDB
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict


class TeamEmployeeDB(Base):
    # Table Employe
    __tablename__ = 'team_employee'
    id_team = Column(Integer, ForeignKey('teams.id_team', ondelete="cascade"), primary_key=True)
    employee_number = Column(String(50), ForeignKey('employee.employee_number', ondelete="cascade"), primary_key=True)

Base.metadata.create_all(bind=engine)


class TeamEmployeeView(BaseModel):
    id_team: int
    employee_number: str


class TeamEmployeeInDB(TeamEmployeeView):
    ...


def get_all_team_employee(db):
    return DataBaseRequest.get_all_data(db, TeamEmployeeDB)


def get_team_employee_by_id(db, id_team: int, employee_number: str):
    data = (db.query(TeamEmployeeDB).where(TeamEmployeeDB.id_team == id_team).
            where(TeamEmployeeDB.employee_number == employee_number).first())
    return data


def get_team_by_employee_number(db, employee_number: str):
    data = (db.query(TeamEmployeeDB, TeamsDB).
            filter(TeamEmployeeDB.id_team == TeamsDB.id_team).
            where(TeamEmployeeDB.employee_number == employee_number).all())
    return data


def get_employee_by_team_name(db, team_name: str):
    data = (db.query(TeamEmployeeDB, TeamsDB, EmployeeDB).
            filter(TeamEmployeeDB.id_team == TeamsDB.id_team).
            filter(TeamEmployeeDB.employee_number == EmployeeDB.employee_number).
            filter(TeamsDB.team_name == team_name).all())

    return data


def get_employee_by_team_id(db, id_team: int):
    data = (db.query(TeamEmployeeDB, TeamsDB, EmployeeDB).
            filter(TeamEmployeeDB.id_team == TeamsDB.id_team).
            filter(TeamEmployeeDB.employee_number == EmployeeDB.employee_number).
            filter(TeamsDB.id_team == id_team).all())
    return data


def post_team_employee(db, team_employee: TeamEmployeeView):
    db_team_employee = TeamEmployeeDB(**team_employee.model_dump(exclude_unset=True))
    return DataBaseRequest.post_data(db, db_team_employee)


def delete_team_employee(db, id_team: int, employee_number: str):
    DataBaseRequest.delete_data(db, TeamEmployeeDB, TeamEmployeeDB.id_team == id_team and TeamEmployeeDB.employee_number == employee_number)
    return True