from app.database import Equipment

from app.database.connexion import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List


router = APIRouter(
    prefix="/equipment",
    tags=["Equipment"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Equipment.EquipmentView])
async def get_all_equipments(db=Depends(get_db)):
    return Equipment.get_all_equipments(db)


@router.get("/{equipment_id}", response_model=Equipment.EquipmentView)
async def get_equipment_by_id(equipment_id: int, db=Depends(get_db)):
    equipment = Equipment.get_equipment_by_id(db, equipment_id)
    if not equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Equipment not found.")

    return equipment


@router.get("/name/{equipment_name}", response_model=Equipment.EquipmentView)
async def get_equipment_by_name(equipment_name: str, db=Depends(get_db)):
    equipment = Equipment.get_equipment_by_name(db, equipment_name)
    if not equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Equipment not found.")

    return equipment


@router.post("/", response_model=Equipment.EquipmentView)
async def post_equipment(equipment: Equipment.EquipmentCreate, db=Depends(get_db)):
    if Equipment.get_equipment_by_id(db, equipment.equipment_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Equipment already exist.")

    return Equipment.post_equipment(db, equipment)


@router.delete("/{equipment_id}")
async def delete_equipment(equipment_id: int, db=Depends(get_db)):
    if not Equipment.get_equipment_by_id(db, equipment_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Equipment not found.")
    return Equipment.delete_equipment(db, equipment_id)


@router.patch("/{equipment_id}", response_model=Equipment.EquipmentView)
async def patch_equipment(equipment_id: int, equipment: Equipment.EquipmentUpdate, db=Depends(get_db)):
    if not Equipment.get_equipment_by_id(db, equipment_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Equipment not found.")
    if equipment.equipment_id and equipment.equipment_id != equipment_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Equipment_id in body and path are different.")

    return Equipment.patch_equipment(db, equipment_id, equipment)
