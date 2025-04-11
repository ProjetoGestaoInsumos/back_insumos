from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.insumo_schema import ItemCreate, ItemOut
from app.services.insumo_service import get_items, create_item
from app.database.db import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[ItemOut])
def read_items(db: Session = Depends(get_db)):
    return get_items(db)

@router.post("/", response_model=ItemOut)
def add_item(insumo: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db, insumo)