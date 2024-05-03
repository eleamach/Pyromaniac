from app.database.Equipment import (EquipmentView, EquipmentInDB, EquipmentUpdate,
                                    get_equipment_by_id, get_equipment_by_type_equipment_id,
                                    get_equipment_by_fire_station_id, get_all_equipment, update_equipment, delete_equipment,
                                    post_equipment, get_equipment_by_name, get_equipment_by_available)
from app.database.connection import get_db
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from typing import List
from app.database.TypeEquipment import TypeEquipmentView, TypeEquipmentInDB, get_type_equipment_by_id
from app.database.FireStation import FireStationView, FireStationInDB, get_fire_station_by_id



router = APIRouter(
    prefix='/api/v1/equipment',
    tags=['Equipment'],
    responses={404: {"description": "Equipment not found"}}
)


@router.get('', response_model=List[EquipmentInDB])
def get_all_equipment_view(db=Depends(get_db)) -> List[EquipmentInDB]:
    return get_all_equipment(db)


@router.get('/id/{id_equipment}', response_model=EquipmentInDB)
def get_equipment_by_id_view(id_equipment: int, db=Depends(get_db)) -> EquipmentInDB:
    equipment = get_equipment_by_id(db, id_equipment)
    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment


@router.get('/type-equipment/{id_type_equipment}', response_model=List[EquipmentInDB])
def get_equipment_by_type_equipment_id_view(id_type_equipment: int, db=Depends(get_db)) -> List[EquipmentInDB]:
    type_equipment = get_type_equipment_by_id(db, id_type_equipment)
    if type_equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    equipment = get_equipment_by_type_equipment_id(db, id_type_equipment)
    return equipment


@router.get('/name/{equipment_name}', response_model=EquipmentInDB)
def get_equipment_by_name_view(equipment_name: str, db=Depends(get_db)) -> EquipmentInDB:
    equipment = get_equipment_by_name(db, equipment_name)
    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment


@router.get('/fire-station/{id_fire_station}', response_model=List[EquipmentInDB])
def get_equipment_by_fire_station_id_view(id_fire_station: int, db=Depends(get_db)) -> List[EquipmentInDB]:
    fire_station = get_fire_station_by_id(db, id_fire_station)
    if fire_station is None:
        raise HTTPException(status_code=404, detail="Fire station not found")
    equipment = get_equipment_by_fire_station_id(db, id_fire_station)
    return equipment


@router.get('/available/{equipment_available}', response_model=List[EquipmentInDB])
def get_equipment_by_available_view(equipment_available: bool, db=Depends(get_db)) -> List[EquipmentInDB]:
    equipment = get_equipment_by_available(db, equipment_available)
    return equipment


@router.post('', response_model=EquipmentInDB)
def post_equipment_view(equipment: EquipmentInDB, db=Depends(get_db)) -> EquipmentInDB:
    if get_type_equipment_by_id(db, equipment.id_type_equipment) is None:
        raise HTTPException(status_code=404, detail="Type equipment not found")
    if get_fire_station_by_id(db, equipment.id_fire_station) is None:
        raise HTTPException(status_code=404, detail="Fire station not found")
    new_equipment = EquipmentInDB(**equipment.model_dump(exclude_unset=True))
    if get_equipment_by_name(db, new_equipment.equipment_name) is not None:
        raise HTTPException(status_code=409, detail="Equipment already exist")
    if get_equipment_by_id(db, new_equipment.id_equipment) is not None:
        raise HTTPException(status_code=410, detail="Duplicate equipment id")
    db_equipment = post_equipment(db, new_equipment)
    return db_equipment


@router.delete('/{id_equipment}', response_model=EquipmentInDB)
def delete_equipment_view(id_equipment: int, db=Depends(get_db)) -> EquipmentView:
    equipment = get_equipment_by_id(db, id_equipment)
    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    delete_equipment(db, id_equipment)
    return equipment


@router.patch('/{id_equipment}', response_model=EquipmentInDB)
def update_equipment_view(id_equipment: int, equipment: EquipmentUpdate, db=Depends(get_db)) -> EquipmentView:
    test_equipment = get_equipment_by_id(db, id_equipment)
    if get_equipment_by_name(db, equipment.equipment_name) is not None:
        raise HTTPException(status_code=409, detail="Equipment Name already exist")
    if test_equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    db_equipment = update_equipment(db, id_equipment, equipment)
    return db_equipment

