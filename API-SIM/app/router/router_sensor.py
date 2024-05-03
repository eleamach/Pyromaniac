from app.database import Sensor
from app.database.connexion import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List


router = APIRouter(
    prefix="/sensor",
    tags=["sensor"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Sensor.SensorView])
async def get_all_sensors(db=Depends(get_db)):
    return Sensor.get_all_sensors(db)


@router.get("/{sensor_id}", response_model=Sensor.SensorView)
async def get_sensor_by_id(sensor_id: int, db=Depends(get_db)):
    sensor = Sensor.get_sensor_by_id(db, sensor_id)
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Sensor not found.")

    return sensor


@router.post("/", response_model=Sensor.SensorView)
async def post_sensor(sensor: Sensor.SensorCreate, db=Depends(get_db)):
    if Sensor.get_sensor_by_id(db, sensor.sensor_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Sensor already exist.")

    return Sensor.post_sensor(db, sensor)


@router.delete("/{sensor_id}")
async def delete_sensor(sensor_id: int, db=Depends(get_db)):
    if not Sensor.get_sensor_by_id(db, sensor_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Sensor not found.")
    return Sensor.delete_sensor(db, sensor_id)


@router.patch("/{sensor_id}", response_model=Sensor.SensorView)
async def patch_sensor(sensor_id: int, sensor: Sensor.SensorUpdate, db=Depends(get_db)):
    if not Sensor.get_sensor_by_id(db, sensor_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Sensor not found.")
    if sensor.sensor_id and sensor.sensor_id != sensor_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Sensor_id in body and path are different.")

    return Sensor.patch_sensor(db, sensor_id, sensor)
