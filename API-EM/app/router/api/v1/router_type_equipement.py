from app.database.TypeEquipment import (get_all_type_equipment,get_type_equipment_by_id, get_type_equipment_by_name,
                                        post_type_equipment, update_type_equipment, delete_type_equipment,
                                        TypeEquipmentView, TypeEquipmentInDB, TypeEquipmentUpdate)
from app.database.connection import get_db
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from app.database.Employee import EmployeeView
from app.database.Teams import TeamsView
from typing import List


router = APIRouter(
    prefix='/api/v1/type-equipment',
    tags=['Type Equipment'],
    responses={404: {"description": "Not found"}}
)


@router.get('', response_model=List[TypeEquipmentView])
def get_all_type_equipment_view(db=Depends(get_db)) -> List[TypeEquipmentInDB]:
    return get_all_type_equipment(db)


@router.get('/id/{id_type_equipment}', response_model=TypeEquipmentView)
def get_type_equipment_by_id_view(id_type_equipment: int, db=Depends(get_db)) -> TypeEquipmentInDB:
    type_equipment = get_type_equipment_by_id(db, id_type_equipment)
    if type_equipment is None:
        raise HTTPException(status_code=404, detail="Type equipment not found")
    return type_equipment


@router.get('/name/{type_equipment_name}', response_model=TypeEquipmentView)
def get_type_equipment_by_name_view(type_equipment_name: str, db=Depends(get_db)) -> TypeEquipmentInDB:
    type_equipment = get_type_equipment_by_name(db, type_equipment_name)
    if type_equipment is None:
        raise HTTPException(status_code=404, detail="Type equipment not found")
    return type_equipment


@router.post('', response_model=TypeEquipmentView)
def post_type_equipment_view(type_equipment: TypeEquipmentInDB, db=Depends(get_db)) -> TypeEquipmentInDB:
    test_type_equipment = get_type_equipment_by_name(db, type_equipment.type_equipment_name)
    if test_type_equipment is not None:
        raise HTTPException(status_code=409, detail="Type equipment already exist")
    new_type_equipment = TypeEquipmentInDB(**type_equipment.model_dump(exclude_unset=True))
    db_type_equipment = post_type_equipment(db, new_type_equipment)
    return db_type_equipment


@router.delete('/{id_type_equipment}', response_model=TypeEquipmentView)
def delete_type_equipment_view(id_type_equipment: int, db=Depends(get_db)) -> bool:
    type_equipment = get_type_equipment_by_id(db, id_type_equipment)
    if type_equipment is None:
        raise HTTPException(status_code=404, detail="Type equipment not found")
    delete_type_equipment(db, id_type_equipment)
    return type_equipment


@router.patch('/{id_type_equipment}', response_model=TypeEquipmentView)
def update_type_equipment_view(id_type_equipment: int, type_equipment: TypeEquipmentUpdate, db=Depends(get_db)) -> TypeEquipmentView:
    test_type_equipment = get_type_equipment_by_id(db, id_type_equipment)
    if test_type_equipment is None:
        raise HTTPException(status_code=404, detail="Type equipment not found")
    db_type_equipment = update_type_equipment(db, id_type_equipment, type_equipment)
    return db_type_equipment
