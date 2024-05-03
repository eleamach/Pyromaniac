from app.database import EventIncidentTeamEquipment, IncidentTeamEquipment
from app.database.connection import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List


router = APIRouter(
    prefix="/event_incident_team_equipment",
    tags=["EventIncidentTeamEquipment"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[EventIncidentTeamEquipment.EventIncidentTeamEquipmentView])
async def get_all_event_incident_team_equipments(db=Depends(get_db)):
    return EventIncidentTeamEquipment.get_all_event_incident_team_equipments(db)


@router.get("/{event_incident_team_equipment_id}", response_model=EventIncidentTeamEquipment.EventIncidentTeamEquipmentView)
async def get_event_incident_team_equipment_by_id(event_incident_team_equipment_id: int, db=Depends(get_db)):
    event_incident_team_equipment = EventIncidentTeamEquipment.get_event_incident_team_equipment_by_id(db, event_incident_team_equipment_id)
    if not event_incident_team_equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="EventIncidentTeamEquipment not found.")

    return event_incident_team_equipment


@router.get("/incident_team_equipment_id/{incident_team_equipment_id}", response_model=List[EventIncidentTeamEquipment.EventIncidentTeamEquipmentView])
async def get_event_incident_team_equipment_by_incident_team_equipment_id(incident_team_equipment_id: int, db=Depends(get_db)):
    event_incident_team_equipment = EventIncidentTeamEquipment.get_event_incident_team_equipment_by_incident_team_equipment_id(db, incident_team_equipment_id)
    if not event_incident_team_equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="EventIncidentTeamEquipment not found.")

    return event_incident_team_equipment


@router.get("/coordinates/{longitude}/{latitude}", response_model=List[EventIncidentTeamEquipment.EventIncidentTeamEquipmentView])
async def get_event_incident_team_equipment_by_coordinates(longitude: float, latitude: float, db=Depends(get_db)):
    event_incident_team_equipment = EventIncidentTeamEquipment.get_event_incident_team_equipment_by_coordinates(db, longitude, latitude)
    if not event_incident_team_equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="EventIncidentTeamEquipment not found.")

    return event_incident_team_equipment


@router.post("/", response_model=EventIncidentTeamEquipment.EventIncidentTeamEquipmentView)
async def post_event_incident_team_equipment(event_incident_team_equipment: EventIncidentTeamEquipment.EventIncidentTeamEquipmentCreate, db=Depends(get_db)):
    if EventIncidentTeamEquipment.get_event_incident_team_equipment_by_id(db, event_incident_team_equipment.id_event_incident_team_equipment):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="EventIncidentTeamEquipment already exist.")

    if not IncidentTeamEquipment.get_incident_team_equipment_by_id(db, event_incident_team_equipment.id_incident_team_equipment):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="IncidentTeamEquipment not found.")

    return EventIncidentTeamEquipment.post_event_incident_team_equipment(db, event_incident_team_equipment)


@router.delete("/{event_incident_team_equipment_id}")
async def delete_event_incident_team_equipment(event_incident_team_equipment_id: int, db=Depends(get_db)):
    if not EventIncidentTeamEquipment.get_event_incident_team_equipment_by_id(db, event_incident_team_equipment_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="EventIncidentTeamEquipment not found.")
    return EventIncidentTeamEquipment.delete_event_incident_team_equipment(db, event_incident_team_equipment_id)


@router.patch("/{event_incident_team_equipment_id}", response_model=EventIncidentTeamEquipment.EventIncidentTeamEquipmentView)
async def patch_event_incident_team_equipment(event_incident_team_equipment_id: int, event_incident_team_equipment: EventIncidentTeamEquipment.EventIncidentTeamEquipmentUpdate, db=Depends(get_db)):
    if not EventIncidentTeamEquipment.get_event_incident_team_equipment_by_id(db, event_incident_team_equipment_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="EventIncidentTeamEquipment not found.")

    if event_incident_team_equipment_id != event_incident_team_equipment.id_event_incident_team_equipment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="EventIncidentTeamEquipment ID mismatch.")

    if not IncidentTeamEquipment.get_incident_team_equipment_by_id(db, event_incident_team_equipment.id_incident_team_equipment):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="IncidentTeamEquipment not found.")

    return EventIncidentTeamEquipment.patch_event_incident_team_equipment(db, event_incident_team_equipment_id, event_incident_team_equipment)