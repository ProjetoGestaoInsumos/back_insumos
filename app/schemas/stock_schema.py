from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class StockCreate(BaseModel):
    item_id: int
    quantity: float
    expiration_date: Optional[datetime] = None

class StockResponse(StockCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True