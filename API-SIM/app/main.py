from fastapi import FastAPI
from app.router import router_incident
from app.router import router_sensor
from app.router import router_sensor_histo
from app.router import router_sensor_event
from app.router import router_incident_sensor_histo
from app.router import router_equipment
from app.router import router_equipment_event
from app.router import router_incident_equipment
from app.router import router_difficulty
from app.router import router_weather
from app.router import router_simulation
from app.router import router_simulation_weather
from app.router import router_simulation_incident


app = FastAPI()
app.include_router(router_incident.router)
app.include_router(router_sensor.router)
app.include_router(router_sensor_histo.router)
app.include_router(router_sensor_event.router)
app.include_router(router_incident_sensor_histo.router)
app.include_router(router_equipment.router)
app.include_router(router_equipment_event.router)
app.include_router(router_incident_equipment.router)
app.include_router(router_difficulty.router)
app.include_router(router_weather.router)
app.include_router(router_simulation.router)
app.include_router(router_simulation_weather.router)
app.include_router(router_simulation_incident.router)

@app.get("/")
async def root():
    return {"message": "Simulation API"}

