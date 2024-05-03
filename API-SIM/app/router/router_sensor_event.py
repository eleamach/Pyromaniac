from app.database import SensorEvent
from app.database.connexion import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List


router = APIRouter(
    prefix="/sensor_event",
    tags=["sensor_event"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[SensorEvent.SensorEventView])
async def get_all_sensor_events(db=Depends(get_db)):
    return SensorEvent.get_all_sensor_events(db)


@router.get("/{id_sensor_event}", response_model=SensorEvent.SensorEventView)
async def get_sensor_event_by_id(id_sensor_event: int, db=Depends(get_db)):
    sensor_event = SensorEvent.get_sensor_event_by_id(db, id_sensor_event)
    if not sensor_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="SensorEvent not found.")

    return sensor_event


@router.post("/", response_model=SensorEvent.SensorEventView)
async def post_sensor_event(sensor_event: SensorEvent.SensorEventCreate, db=Depends(get_db)):

    if SensorEvent.get_sensor_event_by_id(db, sensor_event.id_sensor_event) or SensorEvent.get_sensor_event_by_name(db, sensor_event.event_name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="SensorEvent already exist.")

    return SensorEvent.post_sensor_event(db, sensor_event)


@router.delete("/{id_sensor_event}")
async def delete_sensor_event(id_sensor_event: int, db=Depends(get_db)):
    if not SensorEvent.get_sensor_event_by_id(db, id_sensor_event):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="SensorEvent not found.")
    return SensorEvent.delete_sensor_event(db, id_sensor_event)


@router.patch("/{id_sensor_event}", response_model=SensorEvent.SensorEventView)
async def patch_sensor_event(id_sensor_event: int, sensor_event: SensorEvent.SensorEventUpdate, db=Depends(get_db)):
    if not SensorEvent.get_sensor_event_by_id(db, id_sensor_event):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="SensorEvent not found.")
    if sensor_event.id_sensor_event and sensor_event.id_sensor_event != id_sensor_event:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="SensorEvent_id in body and path are different.")

    return SensorEvent.patch_sensor_event(db, id_sensor_event, sensor_event)

