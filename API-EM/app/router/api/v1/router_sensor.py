from app.database.connection import get_db
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from typing import List
from app.database.Sensor import SensorView, SensorInDB,SensorWithHisto, SensorUpdate, get_all_sensors,get_sensor_by_id, get_sensor_by_coordinates, post_sensor, delete_sensor, update_sensor

router = APIRouter(
    prefix='/api/v1/sensor',
    tags=['Sensor'],
    responses={404: {"description": "Not found"}}
)


@router.get('', response_model=List[SensorInDB])
def get_all_sensors_view(db=Depends(get_db)) -> List[SensorInDB]:
    return get_all_sensors(db)


@router.get('/{id_sensor}', response_model=SensorWithHisto)
def get_sensor_by_id_view(id_sensor: int, db=Depends(get_db)) -> SensorInDB:
    sensor = get_sensor_by_id(db, id_sensor)
    if sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor


@router.get('/coordinates/{longitude}/{latitude}', response_model=SensorInDB)
def get_sensor_by_coordinates_view(longitude: float, latitude: float, db=Depends(get_db)) -> SensorInDB:
    sensor = get_sensor_by_coordinates(db, longitude, latitude)
    if sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor


@router.post('', response_model=SensorInDB)
def post_sensor_view(sensor: SensorInDB, db=Depends(get_db)) -> SensorInDB:
    new_sensor = SensorInDB(**sensor.model_dump(exclude_unset=True))
    db_sensor = post_sensor(db, new_sensor)
    return db_sensor


@router.delete('/{id_sensor}', response_model=SensorView)
def delete_sensor_view(id_sensor: int, db=Depends(get_db)) -> bool:
    sensor = get_sensor_by_id(db, id_sensor)
    if sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    delete_sensor(db, id_sensor)
    return sensor


@router.patch('/{id_sensor}', response_model=SensorView)
def update_sensor_view(id_sensor: int, sensor: SensorUpdate, db=Depends(get_db)) -> SensorView:
    test_sensor = get_sensor_by_id(db, id_sensor)
    if test_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    db_sensor = update_sensor(db, id_sensor, sensor)
    return db_sensor
