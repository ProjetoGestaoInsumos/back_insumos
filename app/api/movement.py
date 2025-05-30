from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.movement import MovementResponse
from app.models.movement import Movement
from app.database.db import get_db

router = APIRouter()

@router.get("/movement", response_model=List[MovementResponse])
def get_movements(
    type: Optional[str] = Query(None),
    pop_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Movement)
    if type:
        query = query.filter(Movement.type == type)
    if pop_id:
        query = query.filter(Movement.pop_id == pop_id)
    return query.all()
