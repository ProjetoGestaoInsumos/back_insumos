from sqlalchemy.orm import Session
from app.models.pop import POP
from app.models.recipe import Recipe
from app.models.item import Item
from app.schemas.pop_schema import POPCreate, POPCheckRequest, POPCheckResponse
from app.models.stock import Stock
from sqlalchemy import func


def create_pop_service(pop_data: POPCreate, db: Session) -> POP:
    """
    Create a new POP entry in the database.
    """
    new_pop = POP(**pop_data.dict())
    db.add(new_pop)
    db.commit()
    db.refresh(new_pop)
    return new_pop


def list_pops_service(db: Session):
    """
    List all POP entries in the database.
    """
    return db.query(POP).all()


def check_pop_service(data: POPCheckRequest, db: Session) -> POPCheckResponse:
    recipe = db.query(Recipe).filter(Recipe.id == data.recipe_id).first()
    if not recipe:
        return POPCheckResponse(
            available={},
            missing={},
            status="recipe not found"
        )

    requested_quantity = data.requested_quantity or 1

    available_items = {}
    missing_items = {}

    for ingredient in recipe.ingredients:
        item = db.query(Item).filter(Item.id == ingredient["item_id"]).first()
        if not item:
            missing_items[f"Item ID {ingredient['item_id']}"] = float(ingredient["quantity"]) * requested_quantity
            continue

        required_quantity = float(ingredient["quantity"]) * requested_quantity

        stock_sum = db.query(func.sum(Stock.quantity)).filter(Stock.item_id == item.id).scalar() or 0

        if stock_sum >= required_quantity:
            available_items[item.name] = required_quantity
        else:
            missing_items[item.name] = required_quantity - stock_sum

    status = "valid" if not missing_items else "missing items"

    return POPCheckResponse(
        available=available_items,
        missing=missing_items,
        status=status
    )