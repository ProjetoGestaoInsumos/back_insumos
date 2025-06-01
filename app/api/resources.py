from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.item_schema import ItemCreate, ItemOut
from app.services.item_service import get_items, create_item
from app.database.db import SessionLocal
from app.database.db import get_db

router = APIRouter()

@router.get("/", response_model=list[ItemOut])
def read_items(db: Session = Depends(get_db)):
    return get_items(db)

@router.post("/", response_model=ItemOut)
def add_item(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db, item)