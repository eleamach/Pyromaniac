from pydantic import BaseModel
from app.database.connexion import Base, engine

from typing import Optional
from sqlalchemy import Column, Integer, String, Float


class DifficultyDB(Base):
    # Table Difficulty
    __tablename__ = 'difficulty'
    difficulty_id = Column(Integer, primary_key=True, index=True, unique=True)
    difficulty_name = Column(String, unique=True)
    difficulty_pound = Column(Float)


Base.metadata.create_all(bind=engine)


class DifficultyBase(BaseModel):
    difficulty_id: int
    difficulty_name: str
    difficulty_pound: float


class DifficultyCreate(DifficultyBase):
    difficulty_id: Optional[int] = None
    difficulty_name: str
    difficulty_pound: Optional[float] = 0.0


class DifficultyUpdate(DifficultyBase):
    difficulty_id: Optional[int] = None
    difficulty_name: Optional[str] = None
    difficulty_pound: Optional[float] = None


class DifficultyView(DifficultyBase):
    ...


def get_all_difficulties(db):
    return db.query(DifficultyDB).all()


def get_difficulty_by_id(db, difficulty_id: int):
    return db.query(DifficultyDB).filter(DifficultyDB.difficulty_id == difficulty_id).first()


def get_difficulty_by_name(db, difficulty_name: str):
    return db.query(DifficultyDB).filter(DifficultyDB.difficulty_name == difficulty_name).first()


def post_difficulty(db, difficulty: DifficultyCreate):
    db_difficulty = DifficultyDB(**difficulty.model_dump(exclude_unset=True))
    db.add(db_difficulty)
    db.commit()
    db.refresh(db_difficulty)
    return db_difficulty


def patch_difficulty(db, difficulty_id: int, difficulty: DifficultyUpdate):
    db_difficulty = (db.query(DifficultyDB).filter(DifficultyDB.difficulty_id == difficulty_id)
                     .update(difficulty.model_dump(exclude_unset=True)))
    db.commit()

    return db.query(DifficultyDB).filter(DifficultyDB.difficulty_id == difficulty_id).first()


def delete_difficulty(db, difficulty_id: int):
    db.query(DifficultyDB).filter(DifficultyDB.difficulty_id == difficulty_id).delete()
    db.commit()
    return {'message': 'Difficulty deleted'}


