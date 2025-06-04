from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.stock import Stock
from app.schemas.stock_schema import StockCreate, StockResponse

router = APIRouter(prefix="/stock", tags=["Stock"])

@router.post("/", response_model=StockResponse)
def create_stock(stock: StockCreate, db: Session = Depends(get_db)):
    new_stock = Stock(**stock.dict())
    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)
    return new_stock

@router.get("/", response_model=list[StockResponse])
def list_stock(db: Session = Depends(get_db)):
    return db.query(Stock).order_by(Stock.item_id).all()

@router.delete("/{id}")
def delete_stock(id: int, db: Session = Depends(get_db)):
    stock = db.query(Stock).filter(Stock.id == id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Lote não encontrado")

    if stock.quantity != 0:
        raise HTTPException(status_code=400, detail="Só é possível excluir lotes com quantidade igual a zero")

    db.delete(stock)
    db.commit()
    return {"detail": "Lote excluído com sucesso"}

@router.put("/{id}", response_model=StockResponse)
def update_stock(id: int, stock_update: StockCreate, db: Session = Depends(get_db)):
    stock = db.query(Stock).filter(Stock.id == id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Lote não encontrado")

    stock.item_id = stock_update.item_id
    stock.quantity = stock_update.quantity
    stock.expiration_date = stock_update.expiration_date

    db.commit()
    db.refresh(stock)
    return stock