from app.database import Incident
from app.database.connexion import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List


router = APIRouter(
    prefix="/incident",
    tags=["Incident"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Incident.IncidentView])
async def get_all_incidents(db=Depends(get_db)):
    return Incident.get_all_incidents(db)


@router.get("/{incident_id}", response_model=Incident.IncidentView)
async def get_incident_by_id(incident_id: int, db=Depends(get_db)):
    incident = Incident.get_incident_by_id(db, incident_id)
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incident not found.")

    return incident


@router.post("/", response_model=Incident.IncidentView)
async def post_incident(incident: Incident.IncidentCreate, db=Depends(get_db)):

    if Incident.get_incident_by_id(db, incident.incident_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Incident already exist.")

    return Incident.post_incident(db, incident)


@router.delete("/{incident_id}")
async def delete_incident(incident_id: int, db=Depends(get_db)):
    if not Incident.get_incident_by_id(db, incident_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incident not found.")
    return Incident.delete_incident(db, incident_id)


@router.patch("/{incident_id}", response_model=Incident.IncidentView)
async def patch_incident(incident_id: int, incident: Incident.IncidentUpdate, db=Depends(get_db)):
    if not Incident.get_incident_by_id(db, incident_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incident not found.")
    if incident.incident_id and incident.incident_id != incident_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incident_id in body and path are different.")

    return Incident.patch_incident(db, incident_id, incident)
