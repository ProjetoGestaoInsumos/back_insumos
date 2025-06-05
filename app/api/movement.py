from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.schemas.movement_schema import MovementResponse
from app.models.movement import Movement
from app.database.db import get_db
from app.models.stock import Stock

router = APIRouter()

@router.get("/movement")
def get_movements(db: Session = Depends(get_db)):
    movements = db.query(Movement).options(
        joinedload(Movement.stock).joinedload(Stock.item),
        joinedload(Movement.user)
    ).all()
    result = []
    for m in movements:
        result.append({
            "id": m.id,
            "stock_id": m.stock_id,
            "quantity": m.quantity,
            "type": m.type,
            "created_at": m.created_at,
            "created_by": m.created_by,
            "item_name": m.stock.item.name if m.stock and m.stock.item else None,
            "user_name": m.user.name if m.user else None,
        })
    return result