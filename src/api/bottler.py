import sqlalchemy
from src import database as db
from fastapi import APIRouter, Depends
from enum import Enum
from pydantic import BaseModel
from src.api import auth

router = APIRouter(
    prefix="/bottler",
    tags=["bottler"],
    dependencies=[Depends(auth.get_api_key)],
)

class PotionInventory(BaseModel):
    potion_type: list[int]
    quantity: int

@router.post("/deliver/{order_id}")
def post_deliver_bottles(potions_delivered: list[PotionInventory], order_id: int):
    """ """
    for potion in potions_delivered:
        if potion.potion_type == [100,0,0,0]:
            for x in range(potion.quantity):
                with db.engine.begin() as connection:
                    connection.execute(sqlalchemy.text("UPDATE global_inventory SET num_red_ml = num_red_ml - 100"))
                    connection.execute(sqlalchemy.text("UPDATE global_inventory SET num_red_potions = num_red_potions + 1"))
        if potion.potion_type == [0,100,0,0]:
            for x in range(potion.quantity):
                with db.engine.begin() as connection:
                    connection.execute(sqlalchemy.text("UPDATE global_inventory SET num_green_ml = num_green_ml - 100"))
                    connection.execute(sqlalchemy.text("UPDATE global_inventory SET num_green_potions = num_green_potions + 1"))
        if potion.potion_type == [0,0,100,0]:
            for x in range(potion.quantity):
                with db.engine.begin() as connection:
                    connection.execute(sqlalchemy.text("UPDATE global_inventory SET num_blue_ml = num_blue_ml - 100"))
                    connection.execute(sqlalchemy.text("UPDATE global_inventory SET num_blue_potions = num_blue_potions + 1"))
        

    print(f"potions delievered: {potions_delivered} order_id: {order_id}")

    return "OK"

@router.post("/plan")
def get_bottle_plan():
    """
    Go from barrel to bottle.
    """

    # Each bottle has a quantity of what proportion of red, blue, and
    # green potion to add.
    # Expressed in integers from 1 to 100 that must sum up to 100.

    # Initial logic: bottle all barrels into red potions.

    with db.engine.begin() as connection:
        redMl = connection.execute(sqlalchemy.text("SELECT num_red_ml FROM global_inventory")).scalar()
        greenMl = connection.execute(sqlalchemy.text("SELECT num_green_ml FROM global_inventory")).scalar()
        blueMl = connection.execute(sqlalchemy.text("SELECT num_blue_ml FROM global_inventory")).scalar()

    redQuantity = (int)(redMl / 100)
    greenQuantity = (int)(greenMl / 100)
    blueQuantity = (int)(blueMl / 100)

    return [
            {
                "potion_type": [100, 0, 0, 0],
                "quantity": redQuantity,
            },
            {
                "potion_type": [0, 100, 0, 0],
                "quantity": greenQuantity,
            },
            {
                "potion_type": [0, 0, 100, 0],
                "quantity": blueQuantity,
            }
        ]

if __name__ == "__main__":
    print(get_bottle_plan())