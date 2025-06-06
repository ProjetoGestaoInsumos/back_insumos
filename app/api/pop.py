from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models.pop import POP
from schemas.pop import POPCreate, POPResponse, POPCheckRequest, POPCheckResponse
from database import get_db
from models.recipe import Recipe
from models.item import Item

router = APIRouter()

@router.post("/pop", response_model=POPResponse)
def create_pop(pop: POPCreate, db: Session = Depends(get_db)):
    db_pop = POP(**pop.dict())
    db.add(db_pop)
    db.commit()
    db.refresh(db_pop)
    return db_pop

@router.get("/pop", response_model=List[POPResponse])
def list_pop(db: Session = Depends(get_db)):
    return db.query(POP).all()

@router.post("/pop/check", response_model=POPCheckResponse)
def check_pop(data: POPCheckRequest, db: Session = Depends(get_db)):
    return {"available": {}, "missing": {}, "status": "valid"}
