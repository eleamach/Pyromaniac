from pydantic import BaseModel
from app.database.connection import Base, engine
from sqlalchemy import Column, Float, String, Integer, DateTime, Boolean, ForeignKey
from typing import Optional, List
from app.database.DataBaseFunction import DataBaseRequest
from sqlalchemy.orm import relationship, backref
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict


class TeamsDB(Base):
    # Table Teams
    __tablename__ = 'teams'
    id_team = Column(Integer, primary_key=True, index=True)
    team_name = Column(String(50), unique=True)
    team_schedule = Column(String(250))
    id_fire_station = Column(Integer, ForeignKey('firestation.id_fire_station', ondelete="cascade"))
    firestation = relationship("FireStationDB", backref=backref("teams", cascade="all, delete-orphan"))


class TeamsView(BaseModel):
    team_name: str
    team_schedule: Optional[str] = None
    id_fire_station: Optional[int] = None


class TeamsInDB(TeamsView):
    id_team: Optional[int] = None



def get_all_teams(db):
    return DataBaseRequest.get_all_data(db, TeamsDB)


def get_team_by_id(db, id_team: int):
    return DataBaseRequest.get_data_by_something(db, TeamsDB, TeamsDB.id_team == id_team)


def get_team_by_name(db, team_name: str):
    return DataBaseRequest.get_data_by_something(db, TeamsDB, TeamsDB.team_name == team_name)


def get_team_by_fire_station_id(db, id_fire_station: int):
    return DataBaseRequest.get_all_data_by_something(db, TeamsDB, TeamsDB.id_fire_station == id_fire_station)


def post_teams(db, teams: TeamsView):
    db_teams = TeamsDB(**teams.model_dump(exclude_unset=True))
    return DataBaseRequest.post_data(db, db_teams)


def delete_team(db, id_team: int):
    DataBaseRequest.delete_data(db, TeamsDB, TeamsDB.id_team == id_team)
    return True


def update_team(db, id_team, teams: TeamsView):
    db.query(TeamsDB).filter(TeamsDB.id_team == id_team).update(teams.model_dump(exclude_unset=True))
    db.commit()
    return get_team_by_id(db, id_team)
