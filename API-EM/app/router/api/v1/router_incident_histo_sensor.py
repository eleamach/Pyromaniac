from app.database.connection import get_db
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from typing import List
from app.database.IncidentSensorHisto import (IncidentSensorHistoView, IncidentSensorHistoInDB,
                                              IncidentSensorHistoUpdate, get_all_incident_sensor_histo,
                                              get_incident_sensor_histo_by_id, get_incident_sensor_histo_by_incident_id,
                                              get_incident_sensor_histo_by_sensor_histo_id, get_incident_sensor_histo_by_sensor_id,
                                              get_incident_sensor_histo_by_sensor_id, post_incident_sensor_histo,
                                              delete_incident_sensor_histo)


router = APIRouter(
    prefix='/api/v1/incident-sensor-histo',
    tags=['Incident Sensor Histo'],
    responses={404: {"description": "Not found"}}
)


@router.get('', response_model=List[IncidentSensorHistoView])
def get_all_incident_sensor_histo_view(db=Depends(get_db)) -> List[IncidentSensorHistoInDB]:
    return get_all_incident_sensor_histo(db)


@router.get('/sensor-histo/{id_incident_sensor_histo}', response_model=IncidentSensorHistoView)
def get_incident_sensor_histo_by_id_view(id_incident_sensor_histo: int, db=Depends(get_db)) -> IncidentSensorHistoInDB:
    incident_sensor_histo = get_incident_sensor_histo_by_id(db, id_incident_sensor_histo)
    if incident_sensor_histo is None:
        raise HTTPException(status_code=404, detail="Incident Sensor Histo not found")
    return incident_sensor_histo


@router.get('/incident/{id_incident}', response_model=List[IncidentSensorHistoView])
def get_incident_sensor_histo_by_incident_id_view(id_incident: int, db=Depends(get_db)) -> IncidentSensorHistoInDB:
    incident_sensor_histo = get_incident_sensor_histo_by_incident_id(db, id_incident)
    if incident_sensor_histo is None:
        raise HTTPException(status_code=404, detail="Incident Sensor Histo not found")
    return incident_sensor_histo


@router.get('/sensor/{id_sensor}', response_model=List[IncidentSensorHistoView])
def get_incident_sensor_histo_by_sensor_id_view(id_sensor: int, db=Depends(get_db)) -> IncidentSensorHistoInDB:
    incident_sensor_histo = get_incident_sensor_histo_by_sensor_id(db, id_sensor)
    if incident_sensor_histo is None:
        raise HTTPException(status_code=404, detail="Incident Sensor Histo not found")
    return incident_sensor_histo


@router.get('/sensor-histo/{id_sensor_histo}/incident/{id_incident}', response_model=List[IncidentSensorHistoView])
def get_incident_sensor_histo_by_sensor_histo_id_view(id_sensor_histo: int, id_incident: int, db=Depends(get_db)) -> IncidentSensorHistoInDB:
    incident_sensor_histo = get_incident_sensor_histo_by_id(db, id_sensor_histo, id_incident)
    if incident_sensor_histo is None:
        raise HTTPException(status_code=404, detail="Incident Sensor Histo not found")
    return incident_sensor_histo


@router.post('', response_model=IncidentSensorHistoView)
def post_incident_sensor_histo_view(incident_sensor_histo: IncidentSensorHistoInDB, db=Depends(get_db)) -> IncidentSensorHistoInDB:
    if get_incident_sensor_histo_by_id(db, incident_sensor_histo.id_incident_sensor_histo) is not None:
        raise HTTPException(status_code=409, detail="Incident Sensor Histo already exist")
    new_incident_sensor_histo = IncidentSensorHistoInDB(**incident_sensor_histo.model_dump(exclude_unset=True))
    db_incident_sensor_histo = post_incident_sensor_histo(db, new_incident_sensor_histo)
    return db_incident_sensor_histo


@router.delete('/{id_incident_sensor_histo}', response_model=IncidentSensorHistoView)
def delete_incident_sensor_histo_view(id_incident_sensor_histo: int, db=Depends(get_db)) -> bool:
    incident_sensor_histo = get_incident_sensor_histo_by_id(db, id_incident_sensor_histo)
    if incident_sensor_histo is None:
        raise HTTPException(status_code=404, detail="Incident Sensor Histo not found")
    delete_incident_sensor_histo(db, id_incident_sensor_histo)
    return incident_sensor_histo

