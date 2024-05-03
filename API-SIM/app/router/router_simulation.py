from app.database import Difficulty
from app.database import Simulation
from app.database.connexion import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List


router = APIRouter(
    prefix="/simulation",
    tags=["Simulation"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Simulation.SimulationView])
async def get_all_simulations(db=Depends(get_db)):
    return Simulation.get_all_simulations(db)


@router.get("/{simulation_id}", response_model=Simulation.SimulationView)
async def get_simulation_by_id(simulation_id: int, db=Depends(get_db)):
    simulation = Simulation.get_simulation_by_id(db, simulation_id)
    if not simulation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Simulation not found.")

    return simulation


@router.get("/difficulty/{difficulty_id}", response_model=Simulation.SimulationView)
async def get_simulation_by_difficulty_id(difficulty_id: int, db=Depends(get_db)):
    simulation = Simulation.get_simulation_by_difficulty_id(db, difficulty_id)
    if not simulation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Simulation not found.")

    return simulation


@router.post("/", response_model=Simulation.SimulationView)
async def post_simulation(simulation: Simulation.SimulationCreate, db=Depends(get_db)):
    if Simulation.get_simulation_by_id(db, simulation.simulation_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Simulation already exist.")

    if not Difficulty.get_difficulty_by_id(db, simulation.difficulty_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Difficulty not found.")

    return Simulation.post_simulation(db, simulation)


@router.delete("/{simulation_id}")
async def delete_simulation(simulation_id: int, db=Depends(get_db)):
    if not Simulation.get_simulation_by_id(db, simulation_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Simulation not found.")
    return Simulation.delete_simulation(db, simulation_id)


@router.patch("/{simulation_id}", response_model=Simulation.SimulationView)
async def patch_simulation(simulation_id: int, simulation: Simulation.SimulationUpdate, db=Depends(get_db)):
    if not Simulation.get_simulation_by_id(db, simulation_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Simulation not found.")

    if simulation.difficulty_id:
        if not Difficulty.get_difficulty_by_id(db, simulation.difficulty_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Difficulty not found.")

    if simulation_id != simulation.simulation_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Simulation ID mismatch.")

    return Simulation.patch_simulation(db, simulation_id, simulation)