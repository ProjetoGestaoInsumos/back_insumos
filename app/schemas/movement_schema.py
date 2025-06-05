from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime
from app.models.movement import MovementType

class MovementCreate(BaseModel):
    stock_id: int
    quantity: int
    type: MovementType
    created_by: int
   

class MovementResponse(BaseModel):
    id: int
    stock_id: int
    quantity: int
    type: MovementType
    created_at: datetime
    created_by: int
    item_name: Optional[str] = None
    user_name: Optional[str] = None
    

    class Config:
        orm_mode = True
