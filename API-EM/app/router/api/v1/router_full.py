from app.database.IncidentFull import IncidentFull, get_incident_full
from app.database.connection import get_db
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from typing import List


router = APIRouter(
    prefix='/api/v1/full',
    tags=['Fire Station'],
    responses={404: {"description": "Not found"}}
)


@router.get('/incident/{incident_id}', response_model=IncidentFull)
async def get_incident_full_view(incident_id: int, db=Depends(get_db)):
    return get_incident_full(db, incident_id)