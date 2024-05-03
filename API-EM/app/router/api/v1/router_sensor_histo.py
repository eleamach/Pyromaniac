from app.database.connection import get_db
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from typing import List
from app.database.SensorHisto import (SensorHistoView, SensorHistoInDB,SensorHistoUpdate, get_all_sensor_histo, get_sensor_histo_by_id,
                                      get_all_non_processed_sensor_histo,get_sensor_histo_by_sensor_id,
                                      get_all_non_processed_sensor_histo_by_sensor_id,
                                      post_sensor_histo, delete_sensor_histo, update_sensor_histo)
from app.database.Sensor import get_sensor_by_id


router = APIRouter(
    prefix='/api/v1/sensor-histo',
    tags=['Sensor Histo'],
    responses={404: {"description": "Not found"}}
)


@router.get('', response_model=List[SensorHistoInDB])
def get_all_sensor_histo_view(db=Depends(get_db)) -> List[SensorHistoInDB]:
    return get_all_sensor_histo(db)


@router.get('/{id_sensor_histo}', response_model=SensorHistoInDB)
def get_sensor_histo_by_id_view(id_sensor_histo: int, db=Depends(get_db)) -> SensorHistoInDB:
    sensor_histo = get_sensor_histo_by_id(db, id_sensor_histo)
    if sensor_histo is None:
        raise HTTPException(status_code=404, detail="Sensor Histo not found")
    return sensor_histo


@router.get('/{id_sensor}/histo', response_model=List[SensorHistoInDB])
def get_sensor_histo_by_sensor_id_view(id_sensor: int, db=Depends(get_db)) -> SensorHistoInDB:
    sensor_histo = get_sensor_histo_by_sensor_id(db, id_sensor)
    if sensor_histo is None:
        raise HTTPException(status_code=404, detail="Sensor Histo not found")
    return sensor_histo


@router.get('/non-processed/', response_model=List[SensorHistoInDB])
def get_sensor_histo_non_processed_view(db=Depends(get_db)) -> List[SensorHistoInDB]:
    return get_all_non_processed_sensor_histo(db)


@router.get('/non-process/{id_sensor}/', response_model=List[SensorHistoInDB])
def get_sensor_histo_non_processed_by_sensor_id_view(id_sensor: int, db=Depends(get_db)) -> SensorHistoInDB:
    if get_sensor_by_id(db, id_sensor) is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    sensor_histo = get_all_non_processed_sensor_histo_by_sensor_id(db, id_sensor)
    if sensor_histo is None:
        raise HTTPException(status_code=404, detail="Sensor Histo not found")
    return sensor_histo


@router.post('', response_model=SensorHistoInDB)
def post_sensor_histo_view(sensor_histo: SensorHistoInDB, db=Depends(get_db)) -> SensorHistoInDB:
    if get_sensor_by_id(db, sensor_histo.id_sensor) is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    if get_sensor_histo_by_id(db, sensor_histo.id_sensor_histo) is not None:
        raise HTTPException(status_code=409, detail="Sensor Histo already exist")
    new_sensor_histo = SensorHistoInDB(**sensor_histo.model_dump(exclude_unset=True))
    db_sensor_histo = post_sensor_histo(db, new_sensor_histo)
    return db_sensor_histo


@router.delete('/{id_sensor_histo}', response_model=SensorHistoInDB)
def delete_sensor_histo_view(id_sensor_histo: int, db=Depends(get_db)) -> bool:
    sensor_histo = get_sensor_histo_by_id(db, id_sensor_histo)
    if sensor_histo is None:
        raise HTTPException(status_code=404, detail="Sensor Histo not found")
    delete_sensor_histo(db, id_sensor_histo)
    return sensor_histo


@router.patch('/{id_sensor_histo}', response_model=SensorHistoInDB)
def update_sensor_histo_view(id_sensor_histo: int, sensor_histo: SensorHistoUpdate, db=Depends(get_db)) -> SensorHistoView:
    test_sensor_histo = get_sensor_histo_by_id(db, id_sensor_histo)
    if test_sensor_histo is None:
        raise HTTPException(status_code=404, detail="Sensor Histo not found")
    db_sensor_histo = update_sensor_histo(db, id_sensor_histo, sensor_histo)
    return db_sensor_histo


