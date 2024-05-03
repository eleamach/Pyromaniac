from app.database import SimulationWeather
from app.database import Simulation
from app.database import Weather
from app.database.connexion import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List


router = APIRouter(
    prefix="/simulation_weather",
    tags=["SimulationWeather"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[SimulationWeather.SimulationWeatherViewID])
async def get_all_simulation_weathers(db=Depends(get_db)):
    return SimulationWeather.get_all_simulation_weathers(db)


@router.get("/simulation_id/{simulation_id}/weather_id/{weather_id}", response_model=SimulationWeather.SimulationWeatherView)
async def get_simulation_weather_by_id(simulation_id: int, weather_id: int, db=Depends(get_db)):
    simulation_weather = SimulationWeather.get_simulation_weather_by_id(db, simulation_id, weather_id)
    if not simulation_weather:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="SimulationWeather not found.")

    return simulation_weather


@router.get("/simulation_id/{simulation_id}", response_model=List[SimulationWeather.SimulationWeatherViewID])
async def get_simulation_weather_by_simulation_id(simulation_id: int, db=Depends(get_db)):
    simulation_weather = SimulationWeather.get_simulation_weather_by_simulation_id(db, simulation_id)
    if not simulation_weather:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="SimulationWeather not found.")

    return simulation_weather


@router.get("/weather_id/{weather_id}", response_model=List[SimulationWeather.SimulationWeatherViewID])
async def get_simulation_weather_by_weather_id(weather_id: int, db=Depends(get_db)):
    simulation_weather = SimulationWeather.get_simulation_weather_by_weather_id(db, weather_id)
    if not simulation_weather:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="SimulationWeather not found.")

    return simulation_weather


@router.post("/", response_model=SimulationWeather.SimulationWeatherView)
async def post_simulation_weather(simulation_weather: SimulationWeather.SimulationWeatherCreate, db=Depends(get_db)):
    if SimulationWeather.get_simulation_weather_by_id(db, simulation_weather.simulation_id, simulation_weather.weather_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="SimulationWeather already exist.")

    if not Simulation.get_simulation_by_id(db, simulation_weather.simulation_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Simulation not found.")

    if not Weather.get_weather_by_id(db, simulation_weather.weather_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Weather not found.")

    return SimulationWeather.post_simulation_weather(db, simulation_weather)


@router.delete("/simulation_id/{simulation_id}/weather_id/{weather_id}")
async def delete_simulation_weather(simulation_id: int, weather_id: int, db=Depends(get_db)):
    if not SimulationWeather.get_simulation_weather_by_id(db, simulation_id, weather_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="SimulationWeather not found.")
    return SimulationWeather.delete_simulation_weather(db, simulation_id, weather_id)