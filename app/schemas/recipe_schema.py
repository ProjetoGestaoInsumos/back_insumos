from pydantic import BaseModel
from typing import List, Optional

class Ingredient(BaseModel):
    item_id: int
    quantity: str

class RecipeBase(BaseModel):
    name: str
    description: Optional[str] = None
    ingredients: List[Ingredient]

class RecipeCreate(RecipeBase):
    pass

class RecipeRead(RecipeBase):
    id: int

    class Config:
        from_attributes = True 
