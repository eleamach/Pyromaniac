from app.database import IncidentEquipment
from app.database.connexion import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database import Equipment
from app.database import EquipmentEvent
from app.database import Incident

router = APIRouter(
    prefix="/incident_equipment",
    tags=["IncidentEquipment"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[IncidentEquipment.IncidentEquipmentView])
async def get_all_incident_equipments(db=Depends(get_db)):
    return IncidentEquipment.get_all_incident_equipments(db)


@router.get("/incident_id/{incident_id}/equipment_id/{equipment_id}/equipment_event_id/{equipment_event_id}", response_model=IncidentEquipment.IncidentEquipmentView)
async def get_incident_equipment_by_id(incident_id: int, equipment_id: int, equipment_event_id: int, db=Depends(get_db)):
    incident_equipment = IncidentEquipment.get_incident_equipment_by_id(db, incident_id, equipment_id, equipment_event_id)
    if not incident_equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="IncidentEquipment not found.")

    return incident_equipment


@router.get("/incident_id/{incident_id}", response_model=List[IncidentEquipment.IncidentEquipmentView])
async def get_incident_equipment_by_incident_id(incident_id: int, db=Depends(get_db)):
    incident_equipment = IncidentEquipment.get_incident_equipment_by_incident_id(db, incident_id)
    if not incident_equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="IncidentEquipment not found.")

    return incident_equipment


@router.get("/equipment_id/{equipment_id}", response_model=List[IncidentEquipment.IncidentEquipmentView])
async def get_incident_equipment_by_equipment_id(equipment_id: int, db=Depends(get_db)):
    incident_equipment = IncidentEquipment.get_incident_equipment_by_equipment_id(db, equipment_id)
    if not incident_equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="IncidentEquipment not found.")

    return incident_equipment


@router.get("/equipment_event_id/{equipment_event_id}", response_model=List[IncidentEquipment.IncidentEquipmentView])
async def get_incident_equipment_by_equipment_event_id(equipment_event_id: int, db=Depends(get_db)):
    incident_equipment = IncidentEquipment.get_incident_equipment_by_equipment_event_id(db, equipment_event_id)
    if not incident_equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="IncidentEquipment not found.")

    return incident_equipment


@router.post("/", response_model=IncidentEquipment.IncidentEquipmentView)
async def post_incident_equipment(incident_equipment: IncidentEquipment.IncidentEquipmentCreate, db=Depends(get_db)):
    if IncidentEquipment.get_incident_equipment_by_id(db, incident_equipment.incident_id, incident_equipment.equipment_id, incident_equipment.equipment_event_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="IncidentEquipment already exists.")

    if Equipment.get_equipment_by_id(db, incident_equipment.equipment_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Equipment not found.")

    if EquipmentEvent.get_equipment_event_by_id(db, incident_equipment.equipment_event_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="EquipmentEvent not found.")

    if Incident.get_incident_by_id(db, incident_equipment.incident_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incident not found.")

    return IncidentEquipment.post_incident_equipment(db, incident_equipment)


@router.delete("/incident_id/{incident_id}/equipment_id/{equipment_id}/equipment_event_id/{equipment_event_id}")
async def delete_incident_equipment(incident_id: int, equipment_id: int, equipment_event_id: int, db=Depends(get_db)):
    incident_equipment = IncidentEquipment.get_incident_equipment_by_id(db, incident_id, equipment_id, equipment_event_id)
    if not incident_equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="IncidentEquipment not found.")

    return IncidentEquipment.delete_incident_equipment(db, incident_id, equipment_id, equipment_event_id)
