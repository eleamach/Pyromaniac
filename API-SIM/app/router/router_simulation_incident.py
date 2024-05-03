from app.database import Incident
from app.database import Simulation
from app.database import SimulationIncident
from app.database.connexion import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List


router = APIRouter(
    prefix="/incident_simulation",
    tags=["IncidentSimulation"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[SimulationIncident.SimulationIncidentViewID])
async def get_all_incident_simulations(db=Depends(get_db)):
    return SimulationIncident.get_all_simulation_incidents(db)


@router.get("/simulation_id/{simulation_id}/incident_id/{incident_id}", response_model=SimulationIncident.SimulationIncidentView)
async def get_incident_simulation_by_id(simulation_id: int, incident_id: int, db=Depends(get_db)):
    incident_simulation = SimulationIncident.get_simulation_incident_by_id(db, simulation_id, incident_id)
    if not incident_simulation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="IncidentSimulation not found.")

    return incident_simulation


@router.get("/simulation_id/{simulation_id}", response_model=List[SimulationIncident.SimulationIncidentViewID])
async def get_incident_simulation_by_simulation_id(simulation_id: int, db=Depends(get_db)):
    incident_simulation = SimulationIncident.get_simulation_incident_by_simulation_id(db, simulation_id)
    if not incident_simulation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="IncidentSimulation not found.")

    return incident_simulation


@router.get("/incident_id/{incident_id}", response_model=List[SimulationIncident.SimulationIncidentViewID])
async def get_incident_simulation_by_incident_id(incident_id: int, db=Depends(get_db)):
    incident_simulation = SimulationIncident.get_simulation_incident_by_incident_id(db, incident_id)
    if not incident_simulation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="IncidentSimulation not found.")

    return incident_simulation


@router.post("/", response_model=SimulationIncident.SimulationIncidentView)
async def post_incident_simulation(incident_simulation: SimulationIncident.SimulationIncidentCreate, db=Depends(get_db)):
    if SimulationIncident.get_simulation_incident_by_id(db, incident_simulation.simulation_id, incident_simulation.incident_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="IncidentSimulation already exist.")

    if not Simulation.get_simulation_by_id(db, incident_simulation.simulation_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Simulation not found.")

    if not Incident.get_incident_by_id(db, incident_simulation.incident_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incident not found.")

    return SimulationIncident.post_simulation_incident(db, incident_simulation)


@router.delete("/simulation_id/{simulation_id}/incident_id/{incident_id}")
async def delete_incident_simulation(simulation_id: int, incident_id: int, db=Depends(get_db)):
    if not SimulationIncident.get_simulation_incident_by_id(db, simulation_id, incident_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="IncidentSimulation not found.")
    return SimulationIncident.delete_simulation_incident(db, simulation_id, incident_id)

