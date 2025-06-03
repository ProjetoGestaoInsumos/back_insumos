from pydantic import BaseModel
from datetime import datetime

class StockCreate(BaseModel):
    item_id: int
    quantity: int
    expiration_date: datetime | None = None

class StockResponse(StockCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True