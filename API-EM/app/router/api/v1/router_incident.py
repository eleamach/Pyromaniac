from app.database.connection import get_db
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from typing import List
from app.database.Incident import (IncidentView, IncidentInDB, IncidentUpdate, get_all_incidents,
                                   get_incident_by_status,
                                   get_incident_by_id, post_incident, delete_incident,
                                   update_incident)

router = APIRouter(
    prefix='/api/v1/incidents',
    tags=['Incidents'],
    responses={404: {"description": "Not found"}}
)


@router.get('', response_model=List[IncidentInDB])
def get_all_incidents_view(db=Depends(get_db)) -> List[IncidentInDB]:
    return get_all_incidents(db)


@router.get('/{id_incident}', response_model=IncidentInDB)
def get_incident_by_id_view(id_incident: int, db=Depends(get_db)) -> IncidentInDB:
    incident = get_incident_by_id(db, id_incident)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@router.get('/status/{status}', response_model=List[IncidentInDB])
def get_incident_by_status_view(status: bool, db=Depends(get_db)) -> List[IncidentInDB]:
    incident = get_incident_by_status(db, status)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@router.post('', response_model=IncidentInDB)
def post_incident_view(incident: IncidentInDB, db=Depends(get_db)) -> IncidentInDB:
    if incident.incident_status is None:
        incident.incident_status = False
    if get_incident_by_id(db, incident.id_incident) is not None:
        raise HTTPException(status_code=409, detail="Duplicate incident id")

    new_incident = IncidentInDB(**incident.model_dump(exclude_unset=True))
    db_incident = post_incident(db, new_incident)
    return db_incident


@router.delete('/{id_incident}', response_model=IncidentInDB)
def delete_incident_view(id_incident: int, db=Depends(get_db)) -> bool:
    incident = get_incident_by_id(db, id_incident)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    delete_incident(db, id_incident)
    return incident


@router.patch('/{id_incident}', response_model=IncidentInDB)
def update_incident_view(id_incident: int, incident: IncidentUpdate, db=Depends(get_db)) -> IncidentView:
    test_incident = get_incident_by_id(db, id_incident)
    if test_incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    db_incident = update_incident(db, id_incident, incident)
    return db_incident
