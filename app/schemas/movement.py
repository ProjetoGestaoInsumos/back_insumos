from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class MovementCreate(BaseModel):
    stock_id: int
    quantity: int
    type: Literal["in", "out"]
    created_by: int
    pop_id: Optional[int] = None

class MovementResponse(BaseModel):
    id: int
    stock_id: int
    quantity: int
    type: str
    created_at: datetime
    created_by: int
    pop_id: Optional[int] = None

    class Config:
        orm_mode = True
