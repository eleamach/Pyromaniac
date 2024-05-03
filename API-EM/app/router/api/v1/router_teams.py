from app.database.Teams import (get_all_teams, get_team_by_id, get_team_by_name, post_teams,delete_team,
                                update_team, get_team_by_fire_station_id, TeamsView, TeamsInDB)
from app.database.connection import get_db
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from typing import List
from app.database.FireStation import get_fire_station_by_id


router = APIRouter(
    prefix='/api/v1/teams',
    tags=['Teams'],
    responses={404: {"description": "Not found"}}
)


@router.get('', response_model=List[TeamsInDB])
def get_all_teams_view(db=Depends(get_db)) -> List[TeamsInDB]:
    return get_all_teams(db)


@router.get('/{id_team}', response_model=TeamsInDB)
def get_team_by_id_view(id_team: int, db=Depends(get_db)) -> TeamsInDB:
    team = get_team_by_id(db, id_team)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.get('/name/{team_name}', response_model=TeamsInDB)
def get_team_by_name_view(team_name: str, db=Depends(get_db)) -> TeamsInDB:
    team = get_team_by_name(db, team_name)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.get('/firestation/{id_fire_station}', response_model=List[TeamsInDB])
def get_team_by_fire_station_id_view(id_fire_station: int, db=Depends(get_db)) -> List[TeamsInDB]:
    team = get_team_by_fire_station_id(db, id_fire_station)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.post('', response_model=TeamsInDB)
def post_teams_view(teams: TeamsInDB, db=Depends(get_db)) -> TeamsInDB:
    test_team = get_team_by_name(db, teams.team_name.lower())
    if test_team is not None:
        raise HTTPException(status_code=409, detail="Team already exist")
    if get_fire_station_by_id(db, teams.id_fire_station) is None:
        raise HTTPException(status_code=404, detail="Fire station not found")
    new_teams = TeamsInDB(**teams.model_dump(exclude_unset=True))
    db_teams = post_teams(db, new_teams)
    return db_teams


@router.delete('/{id_team}', response_model=TeamsView)
def delete_team_view(id_team: int, db=Depends(get_db)) -> bool:
    team = get_team_by_id(db, id_team)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    delete_team(db, id_team)
    return team


@router.patch('/{id_team}', response_model=TeamsView)
def update_team_view(id_team: int, teams: TeamsView, db=Depends(get_db)) -> TeamsView:
    test_team = get_team_by_id(db, id_team)
    if test_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    db_team = update_team(db, id_team, teams)
    return db_team
