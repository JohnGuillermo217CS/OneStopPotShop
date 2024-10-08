import sqlalchemy
from src import database as db
from fastapi import APIRouter

router = APIRouter()


@router.get("/catalog/", tags=["catalog"])
def get_catalog():
    """
    Each unique item combination must have only a single price.
    """

    with db.engine.begin() as connection:
        numRed = connection.execute(sqlalchemy.text("SELECT num_red_potions FROM global_inventory")).scalar()
        numGreen = connection.execute(sqlalchemy.text("SELECT num_green_potions FROM global_inventory")).scalar()
        numBlue = connection.execute(sqlalchemy.text("SELECT num_blue_potions FROM global_inventory")).scalar()

    return [
            {
                "sku": "RED_POTION_0",
                "name": "red potion",
                "quantity": numRed,
                "price": 50,
                "potion_type": [100, 0, 0, 0],
            },
            {
                "sku": "GREEN_POTION_0",
                "name": "green potion",
                "quantity": numGreen,
                "price": 50,
                "potion_type": [0, 100, 0, 0],
            },
            {
                "sku": "BLUE_POTION_0",
                "name": "blue potion",
                "quantity": numBlue,
                "price": 60,
                "potion_type": [0, 0, 100, 0],
            }
        ]
