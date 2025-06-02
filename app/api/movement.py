from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.movement_schema import MovementResponse
from app.models.movement import Movement
from app.database.db import get_db

router = APIRouter()

@router.get("/movement", response_model=List[MovementResponse])
def get_movements(
    
    db: Session = Depends(get_db)
):
    query = db.query(Movement)
   
    return query.all()
