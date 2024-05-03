from pydantic import BaseModel
from app.database.connection import Base, engine
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey


class IncidentTeamEquipmentDB(Base):
    # Table IncidentTeamEquipment
    __tablename__ = 'incident_team_equipment'
    id_incident_team_equipment = Column(Integer, primary_key=True, index=True, unique=True)
    id_incident = Column(Integer, ForeignKey('incident.id_incident', ondelete="cascade"))
    id_team = Column(Integer, ForeignKey('teams.id_team', ondelete="cascade"))
    id_equipment = Column(Integer, ForeignKey('equipment.id_equipment', ondelete="cascade"))


Base.metadata.create_all(bind=engine)


class IncidentTeamEquipmentBase(BaseModel):
    id_incident_team_equipment: int
    id_incident: int
    id_team: int
    id_equipment: int


class IncidentTeamEquipmentCreate(IncidentTeamEquipmentBase):
    id_incident_team_equipment: Optional[int] = None
    id_incident: int
    id_team: int
    id_equipment: int


class IncidentTeamEquipmentView(IncidentTeamEquipmentBase):
    ...



def get_all_incident_team_equipments(db):
    return db.query(IncidentTeamEquipmentDB).all()


def get_incident_team_equipment_by_id(db, id_incident_team_equipment: int):
    return db.query(IncidentTeamEquipmentDB).filter(IncidentTeamEquipmentDB.id_incident_team_equipment == id_incident_team_equipment).first()


def get_incident_team_equipment_by_incident_id(db, id_incident: int):
    return db.query(IncidentTeamEquipmentDB).filter(IncidentTeamEquipmentDB.id_incident == id_incident).all()


def get_incident_team_equipment_by_team_id(db, id_team: int):
    return db.query(IncidentTeamEquipmentDB).filter(IncidentTeamEquipmentDB.id_team == id_team).all()


def get_incident_team_equipment_by_equipment_id(db, id_equipment: int):
    return db.query(IncidentTeamEquipmentDB).filter(IncidentTeamEquipmentDB.id_equipment == id_equipment).all()


def get_incident_team_equipment_by_all_id(db, id_incident: int, id_team: int, id_equipment: int):
    return db.query(IncidentTeamEquipmentDB).filter(IncidentTeamEquipmentDB.id_incident == id_incident,
                                                    IncidentTeamEquipmentDB.id_team == id_team,
                                                    IncidentTeamEquipmentDB.id_equipment == id_equipment).first()


def post_incident_team_equipment(db, incident_team_equipment: IncidentTeamEquipmentCreate):
    db_incident_team_equipment = IncidentTeamEquipmentDB(**incident_team_equipment.model_dump(exclude_unset=True))
    db.add(db_incident_team_equipment)
    db.commit()
    db.refresh(db_incident_team_equipment)
    return db_incident_team_equipment


def delete_incident_team_equipment(db, id_incident_team_equipment: int):
    db.query(IncidentTeamEquipmentDB).filter(IncidentTeamEquipmentDB.id_incident_team_equipment == id_incident_team_equipment).delete()
    db.commit()
    return {"message": "IncidentTeamEquipment deleted"}


def delete_incident_team_equipment_by_all_id(db, id_incident: int, id_team: int, id_equipment: int):
    db.query(IncidentTeamEquipmentDB).filter(IncidentTeamEquipmentDB.id_incident == id_incident,
                                             IncidentTeamEquipmentDB.id_team == id_team,
                                             IncidentTeamEquipmentDB.id_equipment == id_equipment).delete()
    db.commit()
    return {"message": "IncidentTeamEquipment deleted"}

