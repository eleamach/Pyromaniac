from app.database import EquipmentEvent

from app.database.connexion import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List


router = APIRouter(
    prefix="/equipment_event",
    tags=["EquipmentEvent"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[EquipmentEvent.EquipmentEventView])
async def get_all_equipment_events(db=Depends(get_db)):
    return EquipmentEvent.get_all_equipment_events(db)


@router.get("/{equipment_event_id}", response_model=EquipmentEvent.EquipmentEventView)
async def get_equipment_event_by_id(equipment_event_id: int, db=Depends(get_db)):
    equipment_event = EquipmentEvent.get_equipment_event_by_id(db, equipment_event_id)
    if not equipment_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="EquipmentEvent not found.")

    return equipment_event


@router.get("/name/{event_name}", response_model=EquipmentEvent.EquipmentEventView)
async def get_equipment_event_by_name(event_name: str, db=Depends(get_db)):
    equipment_event = EquipmentEvent.get_equipment_event_by_name(db, event_name)
    if not equipment_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="EquipmentEvent not found.")

    return equipment_event


@router.post("/", response_model=EquipmentEvent.EquipmentEventView)
async def post_equipment_event(equipment_event: EquipmentEvent.EquipmentEventCreate, db=Depends(get_db)):
    if EquipmentEvent.get_equipment_event_by_name(db, equipment_event.event_name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="EquipmentEvent already exist.")
    if EquipmentEvent.get_equipment_event_by_id(db, equipment_event.equipment_event_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="EquipmentEvent already exist.")

    return EquipmentEvent.post_equipment_event(db, equipment_event)


@router.delete("/{equipment_event_id}")
async def delete_equipment_event(equipment_event_id: int, db=Depends(get_db)):
    if not EquipmentEvent.get_equipment_event_by_id(db, equipment_event_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="EquipmentEvent not found.")
    return EquipmentEvent.delete_equipment_event(db, equipment_event_id)


@router.patch("/{equipment_event_id}", response_model=EquipmentEvent.EquipmentEventView)
async def patch_equipment_event(equipment_event_id: int, equipment_event: EquipmentEvent.EquipmentEventUpdate, db=Depends(get_db)):
    if not EquipmentEvent.get_equipment_event_by_id(db, equipment_event_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="EquipmentEvent not found.")
    if equipment_event.equipment_event_id and equipment_event.equipment_event_id != equipment_event_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="EquipmentEvent_id in body and path are different.")

    return EquipmentEvent.patch_equipment_event(db, equipment_event_id, equipment_event)

