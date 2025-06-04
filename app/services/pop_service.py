from sqlalchemy.orm import Session
from models.pop import POP
from models.recipe import Recipe
from models.item import Item
from app.schemas.pop_schema import POPCreate, POPCheckRequest, POPCheckResponse


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
    """
    Check item availability for a given recipe and requested quantity.
    Returns available and missing items.
    """

    recipe_id = data.recipe_id
    requested_quantity = data.requested_quantity or 1

    # Get all POPs related to the recipe
    pops = db.query(POP).filter(POP.recipe_id == recipe_id).all()
    if not pops:
        return POPCheckResponse(
            available={},
            missing={},
            status="recipe not found"
        )

    available_items = {}
    missing_items = {}

    for pop in pops:
        item = db.query(Item).filter(Item.id == pop.item_id).first()

        if not item:
            missing_items[f"Item ID {pop.item_id}"] = pop.quantity * requested_quantity
            continue

        required_quantity = pop.quantity * requested_quantity

        if item.stock_quantity >= required_quantity:
            available_items[item.name] = required_quantity
        else:
            missing_items[item.name] = required_quantity - item.stock_quantity

    status = "valid" if not missing_items else "missing items"

    return POPCheckResponse(
        available=available_items,
        missing=missing_items,
        status=status
    )