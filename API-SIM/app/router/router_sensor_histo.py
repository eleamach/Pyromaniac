from app.database import SensorHisto
from app.database.connexion import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List


router = APIRouter(
    prefix="/sensor_histo",
    tags=["SensorHisto"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[SensorHisto.SensorHistoView])
async def get_all_sensor_histos(db=Depends(get_db)):
    return SensorHisto.get_all_sensor_histos(db)


@router.get("/{sensor_histo_id}", response_model=SensorHisto.SensorHistoView)
async def get_sensor_histo_by_id(sensor_histo_id: int, db=Depends(get_db)):
    sensor_histo = SensorHisto.get_sensor_histo_by_id(db, sensor_histo_id)
    if not sensor_histo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="SensorHisto not found.")

    return sensor_histo


@router.post("/", response_model=SensorHisto.SensorHistoView)
async def post_sensor_histo(sensor_histo: SensorHisto.SensorHistoCreate, db=Depends(get_db)):
    if SensorHisto.get_sensor_histo_by_id(db, sensor_histo.sensor_histo_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="SensorHisto already exist.")

    return SensorHisto.post_sensor_histo(db, sensor_histo)


@router.delete("/{sensor_histo_id}")
async def delete_sensor_histo(sensor_histo_id: int, db=Depends(get_db)):
    if not SensorHisto.get_sensor_histo_by_id(db, sensor_histo_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="SensorHisto not found.")
    return SensorHisto.delete_sensor_histo(db, sensor_histo_id)


@router.patch("/{sensor_histo_id}", response_model=SensorHisto.SensorHistoView)
async def patch_sensor_histo(sensor_histo_id: int, sensor_histo: SensorHisto.SensorHistoUpdate, db=Depends(get_db)):
    if not SensorHisto.get_sensor_histo_by_id(db, sensor_histo_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="SensorHisto not found.")
    if sensor_histo.sensor_histo_id and sensor_histo.sensor_histo_id != sensor_histo_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="SensorHisto_id in body and path are different.")

    return SensorHisto.patch_sensor_histo(db, sensor_histo_id, sensor_histo)