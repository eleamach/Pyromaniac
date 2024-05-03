from fastapi.testclient import TestClient
from app.database.connection import Base
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.connection import get_db
from sqlalchemy import create_engine, StaticPool

client = TestClient(app)
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread":False},
                       poolclass=StaticPool,
                       echo=True,
                       future=True)
# Create a session that will be used to interact with the database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def setup():
    Base.metadata.create_all(bind=engine)


def teardown():
    Base.metadata.drop_all(bind=engine)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


# Test fire station

def test_post_fire_station():
    response = client.post(
        "/api/v1/firestation",
        json={
          "fire_station_name": "test",
          "fire_station_longitude": 5,
          "fire_station_latitude": 4.5,
          "id_fire_station": None
        })
    assert response.status_code == 200
    data = response.json()
    assert data["fire_station_name"] == "test"
    assert data["fire_station_longitude"] == 5
    assert data["fire_station_latitude"] == 4.5
    assert data["id_fire_station"] == 1


def test_post_fire_station_sec():
    response = client.post(
        "/api/v1/firestation",
        json={
          "fire_station_name": "test2",
          "fire_station_longitude": 5,
          "fire_station_latitude": 4.5,
          "id_fire_station": None
        })
    assert response.status_code == 200
    data = response.json()
    assert data["fire_station_name"] == "test2"
    assert data["fire_station_longitude"] == 5
    assert data["fire_station_latitude"] == 4.5
    assert data["id_fire_station"] == 2


def test_post_fire_station_already_exist():
    response = client.post(
        "/api/v1/firestation",
        json={
          "fire_station_name": "test",
          "fire_station_longitude": 5,
          "fire_station_latitude": 4.5,
          "id_fire_station": None
        })
    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "Fire station already exist"


def test_get_all_fire_stations():
    response = client.get("/api/v1/firestation")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["fire_station_name"] == "test"
    assert data[0]["fire_station_longitude"] == 5
    assert data[0]["fire_station_latitude"] == 4.5
    assert data[0]["id_fire_station"] == 1
    assert data[1]["fire_station_name"] == "test2"
    assert data[1]["fire_station_longitude"] == 5
    assert data[1]["fire_station_latitude"] == 4.5
    assert data[1]["id_fire_station"] == 2


def test_get_fire_station_by_id():
    response = client.get("/api/v1/firestation/1")
    assert response.status_code == 200
    data = response.json()
    assert data["fire_station_name"] == "test"
    assert data["fire_station_longitude"] == 5
    assert data["fire_station_latitude"] == 4.5
    assert data["id_fire_station"] == 1


def test_get_fire_station_by_id_not_found():
    response = client.get("/api/v1/firestation/9000")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Fire station not found"


def test_get_fire_station_by_name():
    response = client.get("/api/v1/firestation/name/test")
    assert response.status_code == 200
    data = response.json()
    assert data["fire_station_name"] == "test"
    assert data["fire_station_longitude"] == 5
    assert data["fire_station_latitude"] == 4.5
    assert data["id_fire_station"] == 1


def test_get_fire_station_by_name_not_found():
    response = client.get("/api/v1/firestation/name/fuyf")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Fire station not found"


def test_delete_fire_station():
    response = client.delete("/api/v1/firestation/2")
    assert response.status_code == 200
    data = response.json()
    assert data["fire_station_name"] == "test2"
    assert data["fire_station_longitude"] == 5
    assert data["fire_station_latitude"] == 4.5


def test_delete_fire_station_not_found():
    response = client.delete("/api/v1/firestation/2")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Fire station not found"


# Test Teams

def test_post_team():
    response = client.post(
        "/api/v1/teams",
        json={
          "team_name": "Team Test",
          "team_schedule": "255 255 255",
          "id_fire_station": 1,
          "id_team": None
        })
    assert response.status_code == 200
    data = response.json()
    assert data["team_name"] == "team test"
    assert data["team_schedule"] == "255 255 255"
    assert data["id_fire_station"] == 1
    assert data["id_team"] == 1


def test_post_team_sec():
    response = client.post(
        "/api/v1/teams",
        json={
          "team_name": "Team Test 2",
          "team_schedule": "255 255 255",
          "id_fire_station": 1,
          "id_team": None
        })
    assert response.status_code == 200
    data = response.json()
    assert data["team_name"] == "team test 2"
    assert data["team_schedule"] == "255 255 255"
    assert data["id_fire_station"] == 1
    assert data["id_team"] == 2


def test_post_team_already_exist():
    response = client.post(
        "/api/v1/teams",
        json={
          "team_name": "Team Test",
          "team_schedule": "255 255 255",
          "id_fire_station": 1,
          "id_team": None
        })
    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "Team already exist"


def test_post_team_fire_station_not_found():
    response = client.post(
        "/api/v1/teams",
        json={
          "team_name": "Team Test 8",
          "team_schedule": "255 255 255",
          "id_fire_station": 9000,
          "id_team": None
        })
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Fire station not found"


def test_get_all_teams():
    response = client.get("/api/v1/teams")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["team_name"] == "team test"
    assert data[0]["team_schedule"] == "255 255 255"
    assert data[0]["id_fire_station"] == 1
    assert data[0]["id_team"] == 1
    assert data[1]["team_name"] == "team test 2"
    assert data[1]["team_schedule"] == "255 255 255"
    assert data[1]["id_fire_station"] == 1
    assert data[1]["id_team"] == 2


def test_get_team_by_id():
    response = client.get("/api/v1/teams/1")
    assert response.status_code == 200
    data = response.json()
    assert data["team_name"] == "team test"
    assert data["team_schedule"] == "255 255 255"
    assert data["id_fire_station"] == 1
    assert data["id_team"] == 1


def test_get_team_by_id_not_found():
    response = client.get("/api/v1/teams/9000")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Team not found"


def test_get_team_by_name():
    response = client.get("/api/v1/teams/name/team test")
    assert response.status_code == 200
    data = response.json()
    assert data["team_name"] == "team test"
    assert data["team_schedule"] == "255 255 255"
    assert data["id_fire_station"] == 1
    assert data["id_team"] == 1


def test_get_team_by_name_not_found():
    response = client.get("/api/v1/teams/name/team test 8")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Team not found"


def test_delete_team():
    response = client.delete("/api/v1/teams/2")
    assert response.status_code == 200
    data = response.json()
    assert data["team_name"] == "team test 2"
    assert data["team_schedule"] == "255 255 255"
    assert data["id_fire_station"] == 1


def test_delete_team_not_found():
    response = client.delete("/api/v1/teams/2")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Team not found"


def test_patch_team():
    response = client.patch(
        "/api/v1/teams/1",
        json={
          "team_name": "Team Test 3",
          "team_schedule": "255 255 255"
        })
    assert response.status_code == 200
    data = response.json()
    assert data["team_name"] == "team test 3"
    assert data["team_schedule"] == "255 255 255"
    assert data["id_fire_station"] == 1


def test_patch_team_not_found():
    response = client.patch(
        "/api/v1/teams/9000",
        json={
          "team_name": "Team Test 3",
          "team_schedule": "255 255 255"
        })
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Team not found"


# Test Incident

def test_post_incident():
    response = client.post(
        "/api/v1/incidents",
        json={
            "incident_status": False,
            "id_incident": None
        })
    assert response.status_code == 200
    data = response.json()
    assert data["incident_status"] == False
    assert data["id_incident"] == 1


def test_post_incident_sec():
    response = client.post(
        "/api/v1/incidents",
        json={
            "incident_status": False,
            "id_incident": None
        })
    assert response.status_code == 200
    data = response.json()
    assert data["incident_status"] == False
    assert data["id_incident"] == 2


def test_post_incident_tri():
    response = client.post(
        "/api/v1/incidents",
        json={
            "incident_status": False,
            "id_incident": None
        })
    assert response.status_code == 200
    data = response.json()
    assert data["incident_status"] == False
    assert data["id_incident"] == 3

def test_post_incident_already_exist():
    response = client.post(
        "/api/v1/incidents",
        json={
            "incident_status": False,
            "id_incident": 1
        })
    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "Duplicate incident id"


def test_get_all_incidents():
    response = client.get("/api/v1/incidents")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["incident_status"] == False
    assert data[0]["id_incident"] == 1
    assert data[1]["incident_status"] == False
    assert data[1]["id_incident"] == 2


def test_get_incident_by_id():
    response = client.get("/api/v1/incidents/1")
    assert response.status_code == 200
    data = response.json()
    assert data["incident_status"] == False
    assert data["id_incident"] == 1


def test_get_incident_by_id_not_found():
    response = client.get("/api/v1/incidents/9000")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Incident not found"


def test_patch_incident():
    response = client.patch(
        "/api/v1/incidents/1",
        json={
            "incident_status": True
        })
    assert response.status_code == 200
    data = response.json()
    assert data["incident_status"] == True
    assert data["id_incident"] == 1


def test_patch_incident_not_found():
    response = client.patch(
        "/api/v1/incidents/9000",
        json={
            "incident_status": True
        })
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Incident not found"


def test_get_incident_by_status():
    response = client.get("/api/v1/incidents/status/false")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["incident_status"] == False
    assert data[0]["id_incident"] == 2


def test_delete_incident():
    response = client.delete("/api/v1/incidents/2")
    assert response.status_code == 200
    data = response.json()
    assert data["incident_status"] == False
    assert data["id_incident"] == 2


def test_delete_incident_not_found():
    response = client.delete("/api/v1/incidents/9000")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Incident not found"


# Test Incident Team


def test_post_incident_team():
    response = client.post(
        "/api/v1/incident-team",
        json={
            "id_team": 1,
            "id_incident": 1,
            "incident_team_deployment_date": None
        })
    assert response.status_code == 200
    data = response.json()
    assert data["id_team"] == 1
    assert data["id_incident"] == 1
    assert data["incident_team_deployment_date"] == None


    assert response.status_code == 200
    data = response.json()
    assert data["id_team"] == 1
    assert data["id_incident"] == 1
    assert data["incident_team_deployment_date"] == None


def test_get_all_incident_team():
    response = client.get("/api/v1/incident-team")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id_team"] == 1
    assert data[0]["id_incident"] == 1
    assert data[0]["incident_team_deployment_date"] == None


def test_get_incident_team_by_id():
    response = client.get("/api/v1/incident-team/team/1/incident/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id_team"] == 1
    assert data["id_incident"] == 1
    assert data["incident_team_deployment_date"] == None

def test_post_incident_team_sec():
    response = client.post(
        "/api/v1/incident-team",
        json={
            "id_incident": 3,
            "id_team": 1,
            "incident_team_deployment_date": '2021-05-05T00:00:00'
        })
    assert response.status_code == 200
    data = response.json()
    assert data["id_team"] == 1
    assert data["id_incident"] == 3
    assert data["incident_team_deployment_date"] == '2021-05-05T00:00:00'


def test_get_incident_team_by_id_not_found():
    response = client.get("/api/v1/incident-team/team/9000/incident/1")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Incident Team not found"


def test_get_incident_team_by_id_not_found_sec():
    response = client.get("/api/v1/incident-team/team/1/incident/9000")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Incident Team not found"


def test_post_incident_team_already_exist():
    response = client.post(
        "/api/v1/incident-team",
        json={
            "id_team": 1,
            "id_incident": 1,
            "incident_team_deployment_date": None
        })
    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "Incident Team already exist"


def test_post_incident_team_team_not_found():
    response = client.post(
        "/api/v1/incident-team",
        json={
            "id_team": 9000,
            "id_incident": 1,
            "incident_team_deployment_date": None
        })
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Team not found"


def test_post_incident_team_incident_not_found():
    response = client.post(
        "/api/v1/incident-team",
        json={
            "id_team": 1,
            "id_incident": 9000,
            "incident_team_deployment_date": None
        })
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Incident not found"


def test_delete_incident_team():
    response = client.delete("/api/v1/incident-team/team/1/incident/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id_team"] == 1
    assert data["id_incident"] == 1
    assert data["incident_team_deployment_date"] == None


def test_delete_incident_team_not_found():
    response = client.delete("/api/v1/incident-team/team/1/incident/1")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Incident Team not found"


def test_patch_incident_team():
    response = client.patch(
        "/api/v1/incident-team/team/1/incident/3",
        json={
            "incident_team_deployment_date": '2021-05-05T00:00:00'
        })
    assert response.status_code == 200
    data = response.json()
    assert data["id_team"] == 1
    assert data["id_incident"] == 3
    assert data["incident_team_deployment_date"] == '2021-05-05T00:00:00'


def test_patch_incident_team_not_found():
    response = client.patch(
        "/api/v1/incident-team/team/9000/incident/3",
        json={
            "incident_team_deployment_date": '2021-05-05T00:00:00'
        })
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Incident Team not found"


# Test Type Equipment

def test_post_type_equipment():
    response = client.post(
        "/api/v1/type-equipment",
        json={
            "id_type_equipment": None,
            "type_equipment_name": "string",
            "type_equipment_capacity_pers": 0,
            "type_equipment_level_incident": 0,
            "type_equipment_image": "string"
        })
    assert response.status_code == 200
    data = response.json()
    assert data["id_type_equipment"] == 1
    assert data["type_equipment_name"] == "string"
    assert data["type_equipment_capacity_pers"] == 0
    assert data["type_equipment_level_incident"] == 0
    assert data["type_equipment_image"] == "string"


# Test Equipment


def test_post_equipment():
    response = client.post(
        "/api/v1/equipment",
        json={
            "equipment_name": "test",
            "id_type_equipment": 1,
            "id_fire_station": 1,
            "equipment_longitude": 5,
            "equipment_latitude": 4.5,
            "id_equipment": None
        })
    assert response.status_code == 200
    data = response.json()
    assert data["equipment_name"] == "test"
    assert data["id_type_equipment"] == 1
    assert data["id_fire_station"] == 1
    assert data["equipment_longitude"] == 5
    assert data["equipment_latitude"] == 4.5
    assert data["id_equipment"] == 1


def test_post_equipment_sec():
    response = client.post(
        "/api/v1/equipment",
        json={
            "equipment_name": "test2",
            "id_type_equipment": 1,
            "id_fire_station": 1,
            "equipment_longitude": 5,
            "equipment_latitude": 4.5,
            "id_equipment": None
        })
    assert response.status_code == 200
    data = response.json()
    assert data["equipment_name"] == "test2"
    assert data["id_type_equipment"] == 1
    assert data["id_fire_station"] == 1
    assert data["equipment_longitude"] == 5
    assert data["equipment_latitude"] == 4.5
    assert data["id_equipment"] == 2


def test_post_equipment_tri():
    response = client.post(
        "/api/v1/equipment",
        json={
            "equipment_name": "test3",
            "id_type_equipment": 1,
            "id_fire_station": 1,
            "equipment_longitude": 5,
            "equipment_latitude": 4.5,
            "id_equipment": None
        })
    assert response.status_code == 200
    data = response.json()
    assert data["equipment_name"] == "test3"
    assert data["id_type_equipment"] == 1
    assert data["id_fire_station"] == 1
    assert data["equipment_longitude"] == 5
    assert data["equipment_latitude"] == 4.5
    assert data["id_equipment"] == 3


def test_post_equipment_already_exist():
    response = client.post(
        "/api/v1/equipment",
        json={
            "equipment_name": "test",
            "id_type_equipment": 1,
            "id_fire_station": 1,
            "equipment_longitude": 5,
            "equipment_latitude": 4.5,
            "id_equipment": None
        })
    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "Equipment already exist"


def test_post_equipment_fire_station_not_found():
    response = client.post(
        "/api/v1/equipment",
        json={
            "equipment_name": "test",
            "id_type_equipment": 1,
            "id_fire_station": 9000,
            "equipment_longitude": 5,
            "equipment_latitude": 4.5,
            "id_equipment": None
        })
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Fire station not found"


def test_post_equipment_type_equipment_not_found():
    response = client.post(
        "/api/v1/equipment",
        json={
            "equipment_name": "test",
            "id_type_equipment": 9000,
            "id_fire_station": 1,
            "equipment_longitude": 5,
            "equipment_latitude": 4.5,
            "id_equipment": None
        })
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Type equipment not found"


def test_get_all_equipment():
    response = client.get("/api/v1/equipment")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["equipment_name"] == "test"
    assert data[0]["id_type_equipment"] == 1
    assert data[0]["id_fire_station"] == 1
    assert data[0]["equipment_longitude"] == 5
    assert data[0]["equipment_latitude"] == 4.5
    assert data[0]["id_equipment"] == 1
    assert data[1]["equipment_name"] == "test2"
    assert data[1]["id_type_equipment"] == 1
    assert data[1]["id_fire_station"] == 1
    assert data[1]["equipment_longitude"] == 5
    assert data[1]["equipment_latitude"] == 4.5
    assert data[1]["id_equipment"] == 2


def test_get_equipment_by_id():
    response = client.get("/api/v1/equipment/id/1")
    assert response.status_code == 200
    data = response.json()
    assert data["equipment_name"] == "test"
    assert data["id_type_equipment"] == 1
    assert data["id_fire_station"] == 1
    assert data["equipment_longitude"] == 5
    assert data["equipment_latitude"] == 4.5
    assert data["id_equipment"] == 1


def test_get_equipment_by_id_not_found():
    response = client.get("/api/v1/equipment/id/9000")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Equipment not found"


def test_get_equipment_by_name():
    response = client.get("/api/v1/equipment/name/test")
    assert response.status_code == 200
    data = response.json()
    assert data["equipment_name"] == "test"
    assert data["id_type_equipment"] == 1
    assert data["id_fire_station"] == 1
    assert data["equipment_longitude"] == 5
    assert data["equipment_latitude"] == 4.5
    assert data["id_equipment"] == 1


def test_get_equipment_by_name_not_found():
    response = client.get("/api/v1/equipment/name/test8")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Equipment not found"


def test_get_equipment_by_type_equipment_id():
    response = client.get("/api/v1/equipment/type-equipment/1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["equipment_name"] == "test"
    assert data[0]["id_type_equipment"] == 1
    assert data[0]["id_fire_station"] == 1
    assert data[0]["equipment_longitude"] == 5
    assert data[0]["equipment_latitude"] == 4.5
    assert data[0]["id_equipment"] == 1
    assert data[1]["equipment_name"] == "test2"
    assert data[1]["id_type_equipment"] == 1
    assert data[1]["id_fire_station"] == 1
    assert data[1]["equipment_longitude"] == 5
    assert data[1]["equipment_latitude"] == 4.5
    assert data[1]["id_equipment"] == 2


def test_get_equipment_by_type_equipment_id_not_found():
    response = client.get("/api/v1/equipment/type-equipment/9000")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Equipment not found"


def test_get_equipment_by_fire_station_id():
    response = client.get("/api/v1/equipment/fire-station/1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["equipment_name"] == "test"
    assert data[0]["id_type_equipment"] == 1
    assert data[0]["id_fire_station"] == 1
    assert data[0]["equipment_longitude"] == 5
    assert data[0]["equipment_latitude"] == 4.5
    assert data[0]["id_equipment"] == 1
    assert data[1]["equipment_name"] == "test2"
    assert data[1]["id_type_equipment"] == 1
    assert data[1]["id_fire_station"] == 1
    assert data[1]["equipment_longitude"] == 5
    assert data[1]["equipment_latitude"] == 4.5
    assert data[1]["id_equipment"] == 2


def test_get_equipment_by_fire_station_id_not_found():
    response = client.get("/api/v1/equipment/fire-station/9000")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Fire station not found"


def test_delete_equipment():
    response = client.delete("/api/v1/equipment/2")
    assert response.status_code == 200
    data = response.json()
    assert data["equipment_name"] == "test2"
    assert data["id_type_equipment"] == 1
    assert data["id_fire_station"] == 1
    assert data["equipment_longitude"] == 5
    assert data["equipment_latitude"] == 4.5
    assert data["id_equipment"] == 2


def test_delete_equipment_not_found():
    response = client.delete("/api/v1/equipment/9000")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Equipment not found"


def test_patch_equipment():
    response = client.patch(
        "/api/v1/equipment/1",
        json={
            "equipment_name": "tia",
            "id_type_equipment": 1,
            "id_fire_station": 1,
            "equipment_longitude": 5,
            "equipment_latitude": 4.5
        })
    assert response.status_code == 200
    data = response.json()
    assert data["equipment_name"] == "tia"
    assert data["id_type_equipment"] == 1
    assert data["id_fire_station"] == 1
    assert data["equipment_longitude"] == 5
    assert data["equipment_latitude"] == 4.5
    assert data["id_equipment"] == 1

def test_patch_equipment_not_found():
    response = client.patch(
        "/api/v1/equipment/9000",
        json={
            "equipment_name": "test5",
            "id_type_equipment": 1,
            "id_fire_station": 1,
            "equipment_longitude": 5,
            "equipment_latitude": 4.5
        })
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Equipment not found"


def test_patch_equipment_name_already_exist():
    response = client.patch(
        "/api/v1/equipment/1",
        json={
            "equipment_name": "test3",
            "id_type_equipment": 1,
            "id_fire_station": 1,
            "equipment_longitude": 5,
            "equipment_latitude": 4.5
        })
    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "Equipment Name already exist"


# Test Incident Equipment

def test_post_incident_equipment():
    response = client.post(
        "/api/v1/incident-equipment",
        json={
            "id_incident": 1,
            "id_equipment": 1,
        })
    assert response.status_code == 200
    data = response.json()
    assert data["id_incident"] == 1
    assert data["id_equipment"] == 1


def test_post_incident_equipment_sec():
    response = client.post(
        "/api/v1/incident-equipment",
        json={
            "id_incident": 1,
            "id_equipment": 3,
        })
    assert response.status_code == 200
    data = response.json()
    assert data["id_incident"] == 1
    assert data["id_equipment"] == 3


def test_post_incident_equipment_already_exist():
    response = client.post(
        "/api/v1/incident-equipment",
        json={
            "id_incident": 1,
            "id_equipment": 1,
        })
    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "Incident Equipment already exist"


def test_post_incident_equipment_incident_not_found():
    response = client.post(
        "/api/v1/incident-equipment",
        json={
            "id_incident": 9000,
            "id_equipment": 1,
        })
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Incident not found"


def test_post_incident_equipment_equipment_not_found():
    response = client.post(
        "/api/v1/incident-equipment",
        json={
            "id_incident": 1,
            "id_equipment": 9000,
        })
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Equipment not found"


def test_get_all_incident_equipment():
    response = client.get("/api/v1/incident-equipment")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["id_incident"] == 1
    assert data[0]["id_equipment"] == 1
    assert data[1]["id_incident"] == 1
    assert data[1]["id_equipment"] == 3


def test_get_incident_equipment_by_id():
    response = client.get("/api/v1/incident-equipment/incident/1/equipment/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id_incident"] == 1
    assert data["id_equipment"] == 1


def test_get_incident_equipment_by_id_not_found():
    response = client.get("/api/v1/incident-equipment/incident/9000/equipment/1")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Incident Equipment not found"


def test_get_incident_equipment_by_id_not_found_sec():
    response = client.get("/api/v1/incident-equipment/incident/1/equipment/9000")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Incident Equipment not found"


def test_get_incident_equipment_by_incident_id():
    response = client.get("/api/v1/incident-equipment/incident/1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["id_incident"] == 1
    assert data[0]["id_equipment"] == 1
    assert data[1]["id_incident"] == 1
    assert data[1]["id_equipment"] == 3


def test_get_incident_equipment_by_incident_id_not_found():
    response = client.get("/api/v1/incident-equipment/incident/9000")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Incident Equipment not found"


def test_get_incident_equipment_by_equipment_id():
    response = client.get("/api/v1/incident-equipment/equipment/1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id_incident"] == 1
    assert data[0]["id_equipment"] == 1


def test_get_incident_equipment_by_equipment_id_not_found():
    response = client.get("/api/v1/incident-equipment/equipment/9000")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Incident Equipment not found"


def test_delete_incident_equipment():
    response = client.delete("/api/v1/incident-equipment/incident/1/equipment/3")
    assert response.status_code == 200
    data = response.json()
    assert data["id_incident"] == 1
    assert data["id_equipment"] == 3


def test_delete_incident_equipment_not_found():
    response = client.delete("/api/v1/incident-equipment/incident/1/equipment/3")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Incident Equipment not found"