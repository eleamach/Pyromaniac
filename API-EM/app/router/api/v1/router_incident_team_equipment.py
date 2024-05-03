from app.database import IncidentTeamEquipment, Incident, Teams, Equipment
from app.database.connection import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List


router = APIRouter(
    prefix="/incident_team_equipment",
    tags=["IncidentTeamEquipment"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[IncidentTeamEquipment.IncidentTeamEquipmentView])
async def get_all_incident_team_equipments(db=Depends(get_db)):
    return IncidentTeamEquipment.get_all_incident_team_equipments(db)


@router.get("/{incident_team_equipment_id}", response_model=IncidentTeamEquipment.IncidentTeamEquipmentView)
async def get_incident_team_equipment_by_id(incident_team_equipment_id: int, db=Depends(get_db)):
    incident_team_equipment = IncidentTeamEquipment.get_incident_team_equipment_by_id(db, incident_team_equipment_id)
    if not incident_team_equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="IncidentTeamEquipment not found.")

    return incident_team_equipment


@router.get("/incident/{incident_id}", response_model=List[IncidentTeamEquipment.IncidentTeamEquipmentView])
async def get_incident_team_equipment_by_incident_id(incident_id: int, db=Depends(get_db)):
    incident_team_equipment = IncidentTeamEquipment.get_incident_team_equipment_by_incident_id(db, incident_id)
    if not incident_team_equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="IncidentTeamEquipment not found.")

    return incident_team_equipment


@router.get("/team/{team_id}", response_model=List[IncidentTeamEquipment.IncidentTeamEquipmentView])
async def get_incident_team_equipment_by_team_id(team_id: int, db=Depends(get_db)):
    incident_team_equipment = IncidentTeamEquipment.get_incident_team_equipment_by_team_id(db, team_id)
    if not incident_team_equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="IncidentTeamEquipment not found.")

    return incident_team_equipment


@router.get("/equipment/{equipment_id}", response_model=List[IncidentTeamEquipment.IncidentTeamEquipmentView])
async def get_incident_team_equipment_by_equipment_id(equipment_id: int, db=Depends(get_db)):
    incident_team_equipment = IncidentTeamEquipment.get_incident_team_equipment_by_equipment_id(db, equipment_id)
    if not incident_team_equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="IncidentTeamEquipment not found.")

    return incident_team_equipment


@router.get("/all/{incident_id}/{team_id}/{equipment_id}", response_model=IncidentTeamEquipment.IncidentTeamEquipmentView)
async def get_incident_team_equipment_by_all_id(incident_id: int, team_id: int, equipment_id: int, db=Depends(get_db)):
    incident_team_equipment = IncidentTeamEquipment.get_incident_team_equipment_by_all_id(db, incident_id, team_id, equipment_id)
    if not incident_team_equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="IncidentTeamEquipment not found.")

    return incident_team_equipment


@router.post("/", response_model=IncidentTeamEquipment.IncidentTeamEquipmentView)
async def post_incident_team_equipment(incident_team_equipment: IncidentTeamEquipment.IncidentTeamEquipmentCreate, db=Depends(get_db)):
    if IncidentTeamEquipment.get_incident_team_equipment_by_id(db, incident_team_equipment.id_incident_team_equipment):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="IncidentTeamEquipment already exist.")

    if not Incident.get_incident_by_id(db, incident_team_equipment.id_incident):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incident not found.")

    if not Teams.get_team_by_id(db, incident_team_equipment.id_team):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Team not found.")

    if not Equipment.get_equipment_by_id(db, incident_team_equipment.id_equipment):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Equipment not found.")
    if IncidentTeamEquipment.get_incident_team_equipment_by_all_id(db, incident_team_equipment.id_incident, incident_team_equipment.id_team, incident_team_equipment.id_equipment):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="IncidentTeamEquipment already exist.")

    return IncidentTeamEquipment.post_incident_team_equipment(db, incident_team_equipment)


@router.delete("/{incident_team_equipment_id}")
async def delete_incident_team_equipment(incident_team_equipment_id: int, db=Depends(get_db)):
    if not IncidentTeamEquipment.get_incident_team_equipment_by_id(db, incident_team_equipment_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="IncidentTeamEquipment not found.")
    return IncidentTeamEquipment.delete_incident_team_equipment(db, incident_team_equipment_id)


@router.delete("/all/{incident_id}/{team_id}/{equipment_id}")
async def delete_incident_team_equipment_by_all_id(incident_id: int, team_id: int, equipment_id: int, db=Depends(get_db)):
    if not IncidentTeamEquipment.get_incident_team_equipment_by_all_id(db, incident_id, team_id, equipment_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="IncidentTeamEquipment not found.")
    return IncidentTeamEquipment.delete_incident_team_equipment_by_all_id(db, incident_id, team_id, equipment_id)