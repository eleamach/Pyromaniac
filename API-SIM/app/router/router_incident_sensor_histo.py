from app.database import IncidentSensorHisto
from app.database.connexion import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List


router = APIRouter(
    prefix="/incident_sensor_histo",
    tags=["IncidentSensorHisto"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[IncidentSensorHisto.IncidentSensorHistoView])
async def get_all_incident_sensor_histo(db=Depends(get_db)):
    return IncidentSensorHisto.get_all_incident_sensor_histo(db)


@router.get("/incident_id/{incident_id}/sensor_histo_id/{sensor_histo_id}/event_id/{event_id}", response_model=IncidentSensorHisto.IncidentSensorHistoView)
async def get_incident_sensor_histo_by_pk(incident_id: int, sensor_histo_id: int, event_id: int, db=Depends(get_db)):
    incident_sensor_histo = IncidentSensorHisto.get_incident_sensor_histo_by_pk(db, incident_id, sensor_histo_id, event_id)
    if not incident_sensor_histo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="IncidentSensorHisto not found.")

    return incident_sensor_histo


@router.get("/incident_id/{incident_id}", response_model=List[IncidentSensorHisto.IncidentSensorHistoView])
async def get_incident_sensor_histo_by_incident_id(incident_id: int, db=Depends(get_db)):
    return IncidentSensorHisto.get_incident_sensor_histo_by_incident_id(db, incident_id)


@router.get("/sensor_histo_id/{sensor_histo_id}", response_model=List[IncidentSensorHisto.IncidentSensorHistoView])
async def get_incident_sensor_histo_by_sensor_histo_id(sensor_histo_id: int, db=Depends(get_db)):
    return IncidentSensorHisto.get_incident_sensor_histo_by_sensor_histo_id(db, sensor_histo_id)


@router.get("/event_id/{event_id}", response_model=List[IncidentSensorHisto.IncidentSensorHistoView])
async def get_incident_sensor_histo_by_event_id(event_id: int, db=Depends(get_db)):
    return IncidentSensorHisto.get_incident_sensor_histo_by_event_id(db, event_id)


@router.post("/", response_model=IncidentSensorHisto.IncidentSensorHistoView)
async def post_incident_sensor_histo(incident_sensor_histo: IncidentSensorHisto.IncidentSensorHistoCreate, db=Depends(get_db)):
    if IncidentSensorHisto.get_incident_sensor_histo_by_pk(db, incident_sensor_histo.incident_id, incident_sensor_histo.sensor_histo_id, incident_sensor_histo.event_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="IncidentSensorHisto already exist.")

    return IncidentSensorHisto.post_incident_sensor_histo(db, incident_sensor_histo)


@router.delete("/incident_id/{incident_id}/sensor_histo_id/{sensor_histo_id}/event_id/{event_id}")
async def delete_incident_sensor_histo(incident_id: int, sensor_histo_id: int, event_id: int, db=Depends(get_db)):
    if not IncidentSensorHisto.get_incident_sensor_histo_by_pk(db, incident_id, sensor_histo_id, event_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="IncidentSensorHisto not found.")
    return IncidentSensorHisto.delete_incident_sensor_histo(db, incident_id, sensor_histo_id, event_id)


@router.patch("/incident_id/{incident_id}/sensor_histo_id/{sensor_histo_id}/event_id/{event_id}", response_model=IncidentSensorHisto.IncidentSensorHistoView)
async def patch_incident_sensor_histo(incident_id: int, sensor_histo_id: int, event_id: int, incident_sensor_histo: IncidentSensorHisto.IncidentSensorHistoUpdate, db=Depends(get_db)):
    if not IncidentSensorHisto.get_incident_sensor_histo_by_pk(db, incident_id, sensor_histo_id, event_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="IncidentSensorHisto not found.")
    if incident_sensor_histo.incident_id and incident_sensor_histo.incident_id != incident_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incident_id in body and path are different.")
    if incident_sensor_histo.sensor_histo_id and incident_sensor_histo.sensor_histo_id != sensor_histo_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Sensor_histo_id in body and path are different.")
    if incident_sensor_histo.event_id and incident_sensor_histo.event_id != event_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Event_id in body and path are different.")

    return IncidentSensorHisto.patch_incident_sensor_histo(db, incident_id, sensor_histo_id, event_id, incident_sensor_histo)