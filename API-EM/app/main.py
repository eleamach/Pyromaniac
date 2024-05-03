from fastapi import FastAPI
from app.router.api.v1 import router_fire_station
from app.router.api.v1 import router_teams
from app.router.api.v1 import router_employee
from app.router.api.v1 import router_team_employee
from app.router.api.v1 import router_type_equipement
from app.router.api.v1 import router_type_equipment_employee
from app.router.api.v1 import router_equipment
from app.router.api.v1 import router_sensor
from app.router.api.v1 import router_sensor_histo
from app.router.api.v1 import router_incident
from app.router.api.v1 import router_incident_histo_sensor
from app.router.api.v1 import router_incident_team_equipment
from app.router.api.v1 import router_event_incident_team_equipment


app = FastAPI()

app.include_router(router_fire_station.router)
app.include_router(router_teams.router)
app.include_router(router_employee.router)
app.include_router(router_team_employee.router)
app.include_router(router_type_equipement.router)
app.include_router(router_type_equipment_employee.router)
app.include_router(router_equipment.router)
app.include_router(router_sensor.router)
app.include_router(router_sensor_histo.router)
app.include_router(router_incident.router)
app.include_router(router_incident_histo_sensor.router)
app.include_router(router_incident_team_equipment.router)
app.include_router(router_event_incident_team_equipment.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


