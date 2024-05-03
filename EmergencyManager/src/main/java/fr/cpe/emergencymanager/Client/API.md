
# Teams
```json
[
  {
    "team_name": "string",
    "team_schedule": "string",
    "id_fire_station": 0,
    "id_team": 0,
    "members": ["member_number", "member_number"]
  }
]
```
+ Pouvoir faire une recherche de teams par rapport à la caserne de rattachement


# Employees

```json
[
  {
    "employee_first_name": "string",
    "employee_last_name": "string",
    "employee_number": "string",
    "employee_disable": false,
    "teams": [
      {objectTeams}
    ], /* En liste si un pompier peut être dans plusieurs équipes */ 
    "id_fire_station": int /* Si possible */
  }
]
```
+ Pouvoir faire une recherche d'employés d'une équipe donnée.

# Equipment
```json
[
  {
    "equipment_name": "string",
    "id_type_equipment": 0,
    "id_fire_station": 0, /* à retirer */
    "id_equipment": 0, /* à retirer */
    "type_equipment": { objectTypeEquipment },
    "fire_station": { objectCaserne }
  }
]
```

# Sensor
```json
[
  {
    "sensor_longitude": 0,
    "sensor_latitude": 0,
    "id_sensor": 0,
    "last_sensor_histo": { objectSensorHisto } /* /!\ Uniquement le dernier historique traité */
  }
]
```
