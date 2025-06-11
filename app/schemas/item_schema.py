from pydantic import BaseModel
from app.models.item import UnitEnum, CategoryEnum

class ItemCreate(BaseModel):
    name: str
    unit: UnitEnum
    category: CategoryEnum
    description: str

class ItemResponse(ItemCreate):
    id: int

    class Config:
        from_attributes = True
