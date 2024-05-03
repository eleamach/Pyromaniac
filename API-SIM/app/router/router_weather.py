from app.database import Weather
from app.database.connexion import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List


router = APIRouter(
    prefix="/weather",
    tags=["Weather"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Weather.WeatherView])
async def get_all_weathers(db=Depends(get_db)):
    return Weather.get_all_weathers(db)


@router.get("/{weather_id}", response_model=Weather.WeatherView)
async def get_weather_by_id(weather_id: int, db=Depends(get_db)):
    weather = Weather.get_weather_by_id(db, weather_id)
    if not weather:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Weather not found.")

    return weather


@router.get("/name/{weather_name}", response_model=Weather.WeatherView)
async def get_weather_by_name(weather_name: str, db=Depends(get_db)):
    weather = Weather.get_weather_by_name(db, weather_name)
    if not weather:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Weather not found.")

    return weather


@router.post("/", response_model=Weather.WeatherView)
async def post_weather(weather: Weather.WeatherCreate, db=Depends(get_db)):
    if Weather.get_weather_by_id(db, weather.weather_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Weather already exist.")

    if Weather.get_weather_by_name(db, weather.weather_name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Weather already exist.")

    return Weather.post_weather(db, weather)


@router.delete("/{weather_id}")
async def delete_weather(weather_id: int, db=Depends(get_db)):
    if not Weather.get_weather_by_id(db, weather_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Weather not found.")
    return Weather.delete_weather(db, weather_id)


@router.patch("/{weather_id}", response_model=Weather.WeatherView)
async def patch_weather(weather_id: int, weather: Weather.WeatherUpdate, db=Depends(get_db)):
    if not Weather.get_weather_by_id(db, weather_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Weather not found.")

    if weather_id != weather.weather_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Weather id not match.")

    return Weather.patch_weather(db, weather_id, weather)