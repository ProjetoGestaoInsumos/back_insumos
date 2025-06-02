from sqlalchemy.orm import Session
from models.recipe import Recipe
from schemas.recipe_schema import RecipeCreate

def create_recipe(db: Session, recipe_data: RecipeCreate):
    recipe = Recipe(**recipe_data.dict())
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe

def get_recipes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Recipe).offset(skip).limit(limit).all()
