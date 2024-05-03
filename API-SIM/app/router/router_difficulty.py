from app.database import Difficulty
from app.database.connexion import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List


router = APIRouter(
    prefix="/difficulty",
    tags=["Difficulty"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Difficulty.DifficultyView])
async def get_all_difficulties(db=Depends(get_db)):
    return Difficulty.get_all_difficulties(db)


@router.get("/{difficulty_id}", response_model=Difficulty.DifficultyView)
async def get_difficulty_by_id(difficulty_id: int, db=Depends(get_db)):
    difficulty = Difficulty.get_difficulty_by_id(db, difficulty_id)
    if not difficulty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Difficulty not found.")

    return difficulty


@router.get("/name/{difficulty_name}", response_model=Difficulty.DifficultyView)
async def get_difficulty_by_name(difficulty_name: str, db=Depends(get_db)):
    difficulty = Difficulty.get_difficulty_by_name(db, difficulty_name)
    if not difficulty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Difficulty not found.")

    return difficulty


@router.post("/", response_model=Difficulty.DifficultyView)
async def post_difficulty(difficulty: Difficulty.DifficultyCreate, db=Depends(get_db)):
    if Difficulty.get_difficulty_by_id(db, difficulty.difficulty_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Difficulty already exist.")

    if Difficulty.get_difficulty_by_name(db, difficulty.difficulty_name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Difficulty already exist.")

    return Difficulty.post_difficulty(db, difficulty)


@router.delete("/{difficulty_id}")
async def delete_difficulty(difficulty_id: int, db=Depends(get_db)):
    if not Difficulty.get_difficulty_by_id(db, difficulty_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Difficulty not found.")
    return Difficulty.delete_difficulty(db, difficulty_id)


@router.patch("/{difficulty_id}", response_model=Difficulty.DifficultyView)
async def patch_difficulty(difficulty_id: int, difficulty: Difficulty.DifficultyUpdate, db=Depends(get_db)):
    if not Difficulty.get_difficulty_by_id(db, difficulty_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Difficulty not found.")

    if difficulty_id != difficulty.difficulty_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Difficulty ID mismatch.")

    return Difficulty.patch_difficulty(db, difficulty_id, difficulty)