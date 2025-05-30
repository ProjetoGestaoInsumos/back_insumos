from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.item_schema import ItemCreate, ItemOut
from app.services.item_service import get_items, create_item
from app.database.db import SessionLocal
from app.models.item import Item

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
def add_item(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db, item)

@router.delete("/{id}")
def delete_item(id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    # Exemplo de verificação (substitua conforme seu modelo real)
    used_in_recipe = False
    used_in_pop = False
    used_in_lot = False

    if used_in_recipe or used_in_pop or used_in_lot:
        raise HTTPException(status_code=400, detail="Item está sendo utilizado e não pode ser excluído.")

    db.delete(item)
    db.commit()
    return {"detail": "Item excluído com sucesso"}