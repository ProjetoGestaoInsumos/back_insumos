from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.pop import POP
from app.schemas.pop_schema import POPCreate, POPResponse, POPCheckRequest, POPCheckResponse, POPStatusUpdate
from app.database.db import get_db
from app.models.recipe import Recipe
from app.models.item import Item
from app.models.user import User

router = APIRouter()

@router.post("/pop", response_model=POPResponse)
def create_pop(pop: POPCreate, db: Session = Depends(get_db)):
    db_pop = POP(**pop.dict())
    db.add(db_pop)
    db.commit()
    db.refresh(db_pop)

    docente = db.query(User).filter(User.id == db_pop.docente_id).first()
    recipe = db.query(Recipe).filter(Recipe.id == db_pop.recipe_id).first()

    return {
        **db_pop.__dict__,
        "docente_nome": docente.name if docente else "",
        "recipe_name": recipe.name if recipe else ""
    }

@router.get("/pop", response_model=List[POPResponse])
def list_pop(db: Session = Depends(get_db)):
    pops = db.query(POP).all()
    result = []
    for pop in pops:
        docente = db.query(User).filter(User.id == pop.docente_id).first()
        result.append({
            **pop.__dict__,
            "docente_nome": docente.nome if docente else ""
        })
    return result

@router.post("/pop/check", response_model=POPCheckResponse)
def check_pop(data: POPCheckRequest, db: Session = Depends(get_db)):
    return {"available": {}, "missing": {}, "status": "valid"}

@router.put("/pop/{pop_id}/status")
def update_status(pop_id: int, update: POPStatusUpdate, db: Session = Depends(get_db)):
    pop = db.query(POP).filter(POP.id == pop_id).first()
    if not pop:
        raise HTTPException(status_code=404, detail="POP não encontrado")
    pop.status = update.status
    db.commit()
    return {"status": "atualizado"}