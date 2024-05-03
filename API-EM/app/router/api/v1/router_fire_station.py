from app.database.FireStation import get_all_fire_stations, get_fire_station_by_id, get_fire_station_by_name, post_fire_station, delete_fire_station, FireStationView, FireStationInDB
from app.database.connection import get_db
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from typing import List


router = APIRouter(
    prefix='/api/v1/firestation',
    tags=['Fire Station'],
    responses={404: {"description": "Not found"}}
)


@router.get('', response_model=List[FireStationInDB])
def get_all_fire_stations_view(db=Depends(get_db)) -> List[FireStationInDB]:
    return get_all_fire_stations(db)


@router.get('/{id_fire_station}', response_model=FireStationInDB)
def get_fire_station_by_id_view(id_fire_station: int, db=Depends(get_db)) -> FireStationInDB:
    fire_station = get_fire_station_by_id(db, id_fire_station)
    if fire_station is None:
        raise HTTPException(status_code=404, detail="Fire station not found")
    return fire_station


@router.get('/name/{fire_station_name}', response_model=FireStationInDB)
def get_fire_station_by_name_view(fire_station_name: str, db=Depends(get_db)) -> FireStationInDB:
    fire_station = get_fire_station_by_name(db, fire_station_name)
    if fire_station is None:
        raise HTTPException(status_code=404, detail="Fire station not found")
    return fire_station


@router.post('', response_model=FireStationInDB)
def post_fire_station_view(fire_station: FireStationInDB, db=Depends(get_db)) -> FireStationInDB:
    test_fire_station = get_fire_station_by_name(db, fire_station.fire_station_name)
    if test_fire_station is not None:
        raise HTTPException(status_code=409, detail="Fire station already exist")
    if get_fire_station_by_id(db, fire_station.id_fire_station) is not None:
        raise HTTPException(status_code=410, detail="Duplicate fire station id")
    new_fire_station = FireStationInDB(**fire_station.model_dump(exclude_unset=True))
    db_fire_station = post_fire_station(db, new_fire_station)
    return db_fire_station


@router.delete('/{id_fire_station}', response_model=FireStationView)
def delete_fire_station_view(id_fire_station: int, db=Depends(get_db)) -> bool:
    fire_station = get_fire_station_by_id(db, id_fire_station)
    if fire_station is None:
        raise HTTPException(status_code=404, detail="Fire station not found")
    delete_fire_station(db, id_fire_station)
    return fire_station
