from pydantic import BaseModel
from app.database.connexion import Base, engine
from app.database.Difficulty import DifficultyView

from typing import Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, backref



class SimulationDB(Base):
    # Table Simulation
    __tablename__ = 'simulation'
    simulation_id = Column(Integer, primary_key=True, index=True, unique=True)
    difficulty_id = Column(Integer, ForeignKey('difficulty.difficulty_id'))
    difficulty = relationship("DifficultyDB", backref=backref("simulation", cascade="all, delete-orphan"))

    simulation_speed = Column(Float)


Base.metadata.create_all(bind=engine)


class SimulationBase(BaseModel):
    simulation_id: int
    difficulty_id: int
    simulation_speed: float


class SimulationCreate(SimulationBase):
    simulation_id: Optional[int] = None
    difficulty_id: int
    simulation_speed: float


class SimulationUpdate(SimulationBase):
    simulation_id: Optional[int] = None
    difficulty_id: Optional[int] = None
    simulation_speed: Optional[float] = None


class SimulationView(BaseModel):
    simulation_id: int
    difficulty: DifficultyView = []
    simulation_speed: float


def get_all_simulations(db):
    return db.query(SimulationDB).all()


def get_simulation_by_id(db, simulation_id: int):
    return db.query(SimulationDB).filter(SimulationDB.simulation_id == simulation_id).first()


def get_simulation_by_difficulty_id(db, difficulty_id: int):
    return db.query(SimulationDB).filter(SimulationDB.difficulty_id == difficulty_id).first()


def post_simulation(db, simulation: SimulationCreate):
    db_simulation = SimulationDB(**simulation.model_dump(exclude_unset=True))
    db.add(db_simulation)
    db.commit()
    db.refresh(db_simulation)
    return db_simulation


def patch_simulation(db, simulation_id: int, simulation: SimulationUpdate):
    db_simulation = (db.query(SimulationDB).filter(SimulationDB.simulation_id == simulation_id)
                     .update(simulation.model_dump(exclude_unset=True)))
    db.commit()
    return db.query(SimulationDB).filter(SimulationDB.simulation_id == simulation_id).first()


def delete_simulation(db, simulation_id: int):
    db.query(SimulationDB).filter(SimulationDB.simulation_id == simulation_id).delete()
    db.commit()
    return {'message': 'Simulation deleted'}