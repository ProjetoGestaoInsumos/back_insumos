from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.models.recipe import Recipe
from app.models.item import Item
from app.schemas.recipe_schema import RecipeCreate, RecipeRead
from app.database.db import get_db

router = APIRouter()

@router.post("/recipes", response_model=RecipeRead)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    item_ids = [ing.item_id for ing in recipe.ingredients]
    items = db.query(Item).filter(Item.id.in_(item_ids)).all()
    if len(items) != len(item_ids):
        raise HTTPException(status_code=400, detail="Some item_id(s) do not exist.")

    db_recipe = Recipe(
        name=recipe.name,
        description=recipe.description,
        ingredients=[ing.dict() for ing in recipe.ingredients]
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@router.get("/recipes", response_model=List[RecipeRead])
def list_recipes(db: Session = Depends(get_db)):
    return db.query(Recipe).all()

@router.get("/recipes/{id}", response_model=RecipeRead)
def get_recipe(id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.put("/recipes/{id}", response_model=RecipeRead)
def update_recipe(
    id: int,
    recipe_update: RecipeCreate,
    db: Session = Depends(get_db)
):
    # Busca a receita existente
    db_recipe = db.query(Recipe).filter(Recipe.id == id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Valida se todos os items existem
    item_ids = [ing.item_id for ing in recipe_update.ingredients]
    items = db.query(Item).filter(Item.id.in_(item_ids)).all()
    if len(items) != len(item_ids):
        raise HTTPException(status_code=400, detail="Some item_id(s) do not exist.")

    # Atualiza os dados da receita
    db_recipe.name = recipe_update.name
    db_recipe.description = recipe_update.description
    db_recipe.ingredients = [ing.dict() for ing in recipe_update.ingredients]

    db.commit()
    db.refresh(db_recipe)
    return db_recipe