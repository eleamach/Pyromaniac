from pydantic import BaseModel
from app.database.connection import Base, engine
from sqlalchemy import Column, Float, String, Integer, DateTime, Boolean, ForeignKey
from typing import Optional, List
from app.database.DataBaseFunction import DataBaseRequest
from app.database.Incident import IncidentInDB, IncidentDB
from app.database.Equipment import EquipmentInDB, EquipmentDB, get_equipment_by_id
from app.database.Teams import TeamsInDB, TeamsDB, get_team_by_id
from app.database.Sensor import SensorInDB, SensorDB, get_sensor_by_id
from app.database.SensorHisto import SensorHistoInDB, SensorHistoDB
from app.database import IncidentSensorHisto, IncidentTeam, IncidentEquipment, SensorHisto
from datetime import datetime
from fastapi.encoders import jsonable_encoder


class SensorFull(BaseModel):
    id_sensor: int
    id_sensor_histo: List[int] = []
    sensor_histo_last_value: Optional[int] = None
    sensor_histo_last_value_date: Optional[datetime] = None
    sensor_histo_max_value: Optional[int] = None
    sensor_histo_start: Optional[datetime] = None


class IncidentFull(BaseModel):
    id_incident: int
    incident_team: Optional[List[TeamsInDB]] = []
    incident_equipment:  Optional[List[EquipmentInDB]] = []
    incident_sensor:  Optional[List[SensorFull]] = []
    incident_start: Optional[datetime] = None
    incident_level: Optional[int] = None
    incident_status: Optional[bool] = False


def get_incident_full(db, incident_id: int):
    incident_full: IncidentFull = IncidentFull(id_incident=incident_id)
    incident = (db.query(IncidentDB).
                filter(IncidentDB.id_incident == incident_id).first())
    if incident is not None:
        incident_team = IncidentTeam.get_incident_team_by_incident_id(db, incident_id)
        incident_equipment = IncidentEquipment.get_incident_equipment_by_incident_id(db, incident_id)
        incident_sensor_histo = IncidentSensorHisto.get_incident_sensor_histo_by_incident_id(db, incident_id)
        """
        {
          "id_sensor": 2,
          "id_sensor_histo": [18, 19, 20, 26],
          "sensor_histo_last_value": 2,
          "sensor_histo_max_value": 8
        }"""
        news_sensor = []
        for sensor_histo_id in incident_sensor_histo:
            sensor_histo = SensorHisto.get_sensor_histo_by_id(db, sensor_histo_id.id_sensor_histo)

            sensor_a = get_sensor_by_id(db, sensor_histo.id_sensor)
            i,j,k = 0,0,0
            for sensor in news_sensor:
                if sensor.id_sensor == sensor_a.id_sensor:
                    i += 1
                    j = k
                k += 1
            if i == 0:
                news_sensor.append(SensorFull(id_sensor=sensor_a.id_sensor,
                                              id_sensor_histo=[sensor_histo_id.id_sensor_histo],
                                              sensor_histo_max_value=sensor_histo.sensor_histo_value,
                                              sensor_histo_last_value_date=sensor_histo.sensor_histo_date,
                                              sensor_histo_last_value=sensor_histo.sensor_histo_value,
                                              sensor_histo_start=sensor_histo.sensor_histo_date))

            else:
                news_sensor[j].id_sensor_histo.append(sensor_histo_id.id_sensor_histo)

                if news_sensor[j].sensor_histo_max_value is None or news_sensor[j].sensor_histo_max_value < sensor_histo.sensor_histo_value:
                    news_sensor[j].sensor_histo_max_value = sensor_histo.sensor_histo_value
                if news_sensor[j].sensor_histo_last_value_date is None or news_sensor[j].sensor_histo_last_value_date < sensor_histo.sensor_histo_date:
                    news_sensor[j].sensor_histo_last_value_date = sensor_histo.sensor_histo_date
                    news_sensor[j].sensor_histo_last_value = sensor_histo.sensor_histo_value
                if news_sensor[j].sensor_histo_start is None or news_sensor[j].sensor_histo_start > sensor_histo.sensor_histo_date:
                    news_sensor[j].sensor_histo_start = sensor_histo.sensor_histo_date

                incident_full.incident_sensor = news_sensor

        for team in incident_team:
            incident_full.incident_team.append(jsonable_encoder(get_team_by_id(db, team.id_team)))

        for equipment in incident_equipment:
            incident_full.incident_equipment.append(jsonable_encoder(get_equipment_by_id(db, equipment.id_equipment)))

        for sensor in incident_full.incident_sensor:
            if incident_full.incident_start is None or sensor.sensor_histo_start > incident_full.incident_start :
                incident_full.incident_start = sensor.sensor_histo_start
            if incident_full.incident_level is None or sensor.sensor_histo_last_value > incident_full.incident_level :
                incident_full.incident_level = sensor.sensor_histo_last_value
    return incident_full



