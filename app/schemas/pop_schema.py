from pydantic import BaseModel
from typing import Dict, Optional


class POPCreate(BaseModel):
    recipe_id: int
    item_id: int
    quantity: int

    class Config:
        orm_mode = True


class POPResponse(BaseModel):
    id: int
    recipe_id: int
    item_id: int
    quantity: int

    class Config:
        orm_mode = True


class POPCheckRequest(BaseModel):
    recipe_id: int
    requested_quantity: Optional[int] = 1  # optional, default is 1

    class Config:
        orm_mode = True


class POPCheckResponse(BaseModel):
    available: Dict[str, int]
    missing: Dict[str, int]
    status: str

    class Config:
        orm_mode = True