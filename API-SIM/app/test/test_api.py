from fastapi.testclient import TestClient
from app.database.connexion import Base
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.connexion import get_db
from sqlalchemy import create_engine, StaticPool

client = TestClient(app)
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False},
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


# Incident

def test_create_incident():
    response = client.post(
        "/incident/",
        json={"incident_id": 1, "incident_status": False},
    )
    assert response.status_code == 200
    assert response.json() == {"incident_id": 1, "incident_status": False}


def test_create_incident_second():
    response = client.post(
        "/incident/",
        json={"incident_id": 2, "incident_status": False},
    )
    assert response.status_code == 200
    assert response.json() == {"incident_id": 2, "incident_status": False}


def test_create_incident_conflict():
    response = client.post(
        "/incident/",
        json={"incident_id": 1, "incident_status": False},
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Incident already exist."}


def test_get_all_incidents():
    response = client.get("/incident/")
    assert response.status_code == 200
    assert response.json() == [{"incident_id": 1, "incident_status": False},
                               {"incident_id": 2, "incident_status": False}]


def test_get_incident_by_id():
    response = client.get("/incident/1")
    assert response.status_code == 200
    assert response.json() == {"incident_id": 1, "incident_status": False}


def test_get_incident_by_id_not_found():
    response = client.get("/incident/404")
    assert response.status_code == 404
    assert response.json() == {"detail": "Incident not found."}


def test_delete_incident():
    response = client.delete("/incident/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Incident deleted successfully."}


def test_delete_incident_not_found():
    response = client.delete("/incident/404")
    assert response.status_code == 404
    assert response.json() == {"detail": "Incident not found."}


def test_patch_incident():
    response = client.patch(
        "/incident/2",
        json={"incident_id": 2, "incident_status": True},
    )
    assert response.status_code == 200
    assert response.json() == {"incident_id": 2, "incident_status": True}


def test_patch_incident_not_found():
    response = client.patch(
        "/incident/404",
        json={"incident_id": 404, "incident_status": True},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Incident not found."}


def test_patch_incident_id_different():
    response = client.patch(
        "/incident/2",
        json={"incident_id": 1, "incident_status": True},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Incident_id in body and path are different."}


# Sensor

def test_create_sensor():
    response = client.post(
        "/sensor/",
        json={"sensor_id": None, "sensor_longitude": 0.0, "sensor_latitude": 0.0},
    )
    assert response.status_code == 200
    assert response.json() == {"sensor_id": 1,
                               "sensor_longitude": 0.0,
                               "sensor_latitude": 0.0}



def test_create_sensor_second():
    response = client.post(
        "/sensor/",
        json={"sensor_id": None,
              "sensor_longitude": 1.0,
              "sensor_latitude": 1.0},
    )
    assert response.status_code == 200
    assert response.json() == {"sensor_id": 2,
                               "sensor_longitude": 1.0,
                               "sensor_latitude": 1.0}



def test_create_sensor_conflict():
    response = client.post(
        "/sensor/",
        json={"sensor_id": 1,
              "sensor_longitude": 0.0,
              "sensor_latitude": 0.0},
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Sensor already exist."}


def test_get_all_sensors():
    response = client.get("/sensor/")
    assert response.status_code == 200
    assert response.json() == [{"sensor_id": 1,
                                "sensor_longitude": 0.0,
                                "sensor_latitude": 0.0},
                               {"sensor_id": 2,
                                "sensor_longitude": 1.0,
                                "sensor_latitude": 1.0}]



def test_get_sensor_by_id():
    response = client.get("/sensor/1")
    assert response.status_code == 200
    assert response.json() == {"sensor_id": 1,
                               "sensor_longitude": 0.0,
                               "sensor_latitude": 0.0}



def test_get_sensor_by_id_not_found():
    response = client.get("/sensor/404")
    assert response.status_code == 404
    assert response.json() == {"detail": "Sensor not found."}


def test_delete_sensor():
    response = client.delete("/sensor/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Sensor deleted successfully."}


def test_delete_sensor_not_found():
    response = client.delete("/sensor/404")
    assert response.status_code == 404
    assert response.json() == {"detail": "Sensor not found."}


def test_patch_sensor():
    response = client.patch("/sensor/2",
                            json={"sensor_id": 2,
                                  "sensor_longitude": 2.0,
                                  "sensor_latitude": 2.0})

    assert response.status_code == 200
    assert response.json() == {"sensor_id": 2,
                               "sensor_longitude": 2.0,
                               "sensor_latitude": 2.0}


def test_patch_sensor_not_found():
    response = client.patch("/sensor/404",
                            json={"sensor_id": 404,
                                  "sensor_longitude": 2.0,
                                  "sensor_latitude": 2.0})

    assert response.status_code == 404
    assert response.json() == {"detail": "Sensor not found."}


def test_patch_sensor_id_different():
    response = client.patch("/sensor/2",
                            json={"sensor_id": 1,
                                  "sensor_longitude": 2.0,
                                  "sensor_latitude": 2.0})

    assert response.status_code == 400
    assert response.json() == {"detail": "Sensor_id in body and path are different."}


# SensorHisto


def test_create_sensor_histo():
    response = client.post(
        "/sensor_histo/",
        json={"sensor_histo_id": None,
              "sensor_histo_date": "2023-12-19T12:54:24",
              "sensor_histo_value": 1.0,
              "sensor_histo_is_processed": False,
              "sensor_id": 2},

    )
    assert response.status_code == 200
    assert response.json() == {"sensor_histo_id": 1,
                               "sensor_histo_date": "2023-12-19T12:54:24",
                               "sensor_histo_value": 1.0,
                               "sensor_histo_is_processed": False,
                               "sensor_id": 2,
                               "sensor": {"sensor_id": 2,
                                          "sensor_longitude": 2.0,
                                          "sensor_latitude": 2.0}}



def test_create_sensor_histo_second():
    response = client.post(
        "/sensor_histo/",
        json={"sensor_histo_id": None,
              "sensor_histo_date": "2023-12-19T12:54:24",
              "sensor_histo_value": 2.0,
              "sensor_histo_is_processed": False,
              "sensor_id": 2},

    )
    assert response.status_code == 200
    assert response.json() == {"sensor_histo_id": 2,
                               "sensor_histo_date": "2023-12-19T12:54:24",
                               "sensor_histo_value": 2.0,
                               "sensor_histo_is_processed": False,
                               "sensor_id": 2,
                               "sensor": {"sensor_id": 2,
                                          "sensor_longitude": 2.0,
                                          "sensor_latitude": 2.0}}



def test_create_sensor_histo_conflict():
    response = client.post(
        "/sensor_histo/",
        json={"sensor_histo_id": 1,
              "sensor_histo_date": "2023-12-19T12:54:24",
              "sensor_histo_value": 1.0,
              "sensor_histo_is_processed": False,
              "sensor_id": 1},
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "SensorHisto already exist."}


def test_get_all_sensor_histo():
    response = client.get("/sensor_histo/")
    assert response.status_code == 200
    assert response.json() == [{"sensor_histo_id": 1,
                                "sensor_histo_date": "2023-12-19T12:54:24",
                                "sensor_histo_value": 1.0,
                                "sensor_histo_is_processed": False,
                                "sensor_id": 2,
                                "sensor": {
                                        "sensor_id": 2,
                                        "sensor_longitude": 2.0,
                                        "sensor_latitude": 2.0}},

                               {"sensor_histo_id": 2,
                                "sensor_histo_date": "2023-12-19T12:54:24",
                                "sensor_histo_value": 2.0,
                                "sensor_histo_is_processed": False,
                                "sensor_id": 2,
                                "sensor": {
                                        "sensor_id": 2,
                                        "sensor_longitude": 2.0,
                                        "sensor_latitude": 2.0}}]



def test_get_sensor_histo_by_id():
    response = client.get("/sensor_histo/1")
    assert response.status_code == 200
    assert response.json() == {"sensor_histo_id": 1,
                               "sensor_histo_date": "2023-12-19T12:54:24",
                               "sensor_histo_value": 1.0,
                               "sensor_histo_is_processed": False,
                               "sensor_id": 2,
                                "sensor": {
                                        "sensor_id": 2,
                                        "sensor_longitude": 2.0,
                                        "sensor_latitude": 2.0}}



def test_get_sensor_histo_by_id_not_found():
    response = client.get("/sensor_histo/404")
    assert response.status_code == 404
    assert response.json() == {"detail": "SensorHisto not found."}


def test_delete_sensor_histo():
    response = client.delete("/sensor_histo/1")
    assert response.status_code == 200
    assert response.json() == {"message": "SensorHisto deleted successfully."}


def test_delete_sensor_histo_not_found():
    response = client.delete("/sensor_histo/404")
    assert response.status_code == 404
    assert response.json() == {"detail": "SensorHisto not found."}


def test_patch_sensor_histo():
    response = client.patch("/sensor_histo/2",
                            json={"sensor_histo_id": 2,
                                  "sensor_histo_date": "2023-12-19T12:54:24",
                                  "sensor_histo_value": 3.0,
                                  "sensor_histo_is_processed": False,
                                  "sensor_id": 2})


    assert response.status_code == 200
    assert response.json() == {"sensor_histo_id": 2,
                               "sensor_histo_date": "2023-12-19T12:54:24",
                               "sensor_histo_value": 3.0,
                               "sensor_histo_is_processed": False,
                               "sensor_id": 2,
                                "sensor": {
                                        "sensor_id": 2,
                                        "sensor_longitude": 2.0,
                                        "sensor_latitude": 2.0}}



def test_patch_sensor_histo_not_found():
    response = client.patch("/sensor_histo/404",
                            json={"sensor_histo_id": 404,
                                  "sensor_histo_date": "2023-12-19T12:54:24",
                                  "sensor_histo_value": 3.0,
                                  "sensor_histo_is_processed": False,
                                  "sensor_id": 2})


    assert response.status_code == 404
    assert response.json() == {"detail": "SensorHisto not found."}


def test_patch_sensor_histo_id_different():
    response = client.patch("/sensor_histo/2",
                            json={"sensor_histo_id": 1,
                                  "sensor_histo_date": "2023-12-19T12:54:24",
                                  "sensor_histo_value": 3.0,
                                  "sensor_histo_is_processed": False,
                                  "sensor_id": 2,
                                  "sensor": {
                                        "sensor_id": 2,
                                        "sensor_longitude": 2.0,
                                        "sensor_latitude": 2.0}})

    assert response.status_code == 400
    assert response.json() == {"detail": "SensorHisto_id in body and path are different."}


# IncidentSensorHisto
def test_create_incident_sensor_histo():
    response = client.post(
        "/incident_sensor_histo/",
        json={"incident_id": 1,
              "sensor_histo_id": 1,
              "event_id": 1},
    )
    assert response.status_code == 200
    assert response.json() == {"incident_id": 1,
                               "sensor_histo_id": 1,
                               "event_id": 1,
                               "incident": {"incident_id": 1,
                                            "incident_status": False},
                               "sensor_histo": {"sensor_histo_id": 1,
                                                "sensor_histo_date": "2023-12-19T12:54:24",
                                                "sensor_histo_value": 1.0,
                                                "sensor_histo_is_processed": False,
                                                "sensor_id": 2,
                                                "sensor": {"sensor_id": 2,
                                                           "sensor_longitude": 2.0,
                                                           "sensor_latitude": 2.0}}}

