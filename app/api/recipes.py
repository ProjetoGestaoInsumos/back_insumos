from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from models.recipe import Recipe
from schemas.recipe import RecipeCreate, RecipeResponse
from database import get_db
from models.item import Item  

router = APIRouter()

@router.post("/recipes", response_model=RecipeResponse)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    # validate if all item_ids exist
    item_ids = [ing.item_id for ing in recipe.ingredients]
    items = db.query(Item).filter(Item.id.in_(item_ids)).all()
    if len(items) != len(item_ids):
        raise HTTPException(status_code=400, detail="Some item_id(s) do not exist.")

    db_recipe = Recipe(name=recipe.name, description=recipe.description, ingredients=[ing.dict() for ing in recipe.ingredients])
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@router.get("/recipes", response_model=List[RecipeResponse])
def list_recipes(db: Session = Depends(get_db)):
    return db.query(Recipe).all()

@router.get("/recipes/{id}", response_model=RecipeResponse)
def get_recipe(id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe
