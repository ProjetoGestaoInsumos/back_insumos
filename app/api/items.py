from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.item_schema import ItemCreate, ItemResponse
from app.database.db import get_db
from app.models.item import Item

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/", response_model=list[ItemResponse])
def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()

@router.post("/", response_model=ItemResponse)
def add_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{id}")
def delete_item(id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    used_in_recipe = False
    used_in_pop = False
    used_in_lot = False

    if used_in_recipe or used_in_pop or used_in_lot:
        raise HTTPException(status_code=400, detail="Item está sendo utilizado e não pode ser excluído.")

    db.delete(item)
    db.commit()
    return {"detail": "Item excluído com sucesso"}