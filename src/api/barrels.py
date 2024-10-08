import sqlalchemy
from src import database as db
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth

router = APIRouter(
    prefix="/barrels",
    tags=["barrels"],
    dependencies=[Depends(auth.get_api_key)],
)

class Barrel(BaseModel):
    sku: str

    ml_per_barrel: int
    potion_type: list[int]
    price: int

    quantity: int

@router.post("/deliver/{order_id}")
def post_deliver_barrels(barrels_delivered: list[Barrel], order_id: int):
    """ """
    for barrel in barrels_delivered:
        if barrel.potion_type == [100,0,0,0]:
            for i in range(barrel.quantity):
                with db.engine.begin() as connection:
                    connection.execute(sqlalchemy.text("UPDATE global_inventory SET num_red_ml = num_red_ml + :ml_per_barrel"), {"ml_per_barrel": barrel.ml_per_barrel})
                    connection.execute(sqlalchemy.text("UPDATE global_inventory SET gold = gold - :price"), {"price": barrel.price})
        if barrel.potion_type == [0,100,0,0]:
            for i in range(barrel.quantity):
                with db.engine.begin() as connection:
                    connection.execute(sqlalchemy.text("UPDATE global_inventory SET num_green_ml = num_green_ml + :ml_per_barrel"), {"ml_per_barrel": barrel.ml_per_barrel})
                    connection.execute(sqlalchemy.text("UPDATE global_inventory SET gold = gold - :price"), {"price": barrel.price})
        if barrel.potion_type == [0,0,100,0]:
            for i in range(barrel.quantity):
                with db.engine.begin() as connection:
                    connection.execute(sqlalchemy.text("UPDATE global_inventory SET num_blue_ml = num_blue_ml + :ml_per_barrel"), {"ml_per_barrel": barrel.ml_per_barrel})
                    connection.execute(sqlalchemy.text("UPDATE global_inventory SET gold = gold - :price"), {"price": barrel.price})
    print(f"barrels delievered: {barrels_delivered} order_id: {order_id}")

    return "OK"

# Gets called once a day
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Barrel]):
    """ """
    print(wholesale_catalog)

    with db.engine.begin() as connection:
        gold = connection.execute(sqlalchemy.text("SELECT gold FROM global_inventory")).scalar()
        numRedPots = connection.execute(sqlalchemy.text("SELECT num_red_potions FROM global_inventory")).scalar()
        numGreenPots = connection.execute(sqlalchemy.text("SELECT num_green_potions FROM global_inventory")).scalar()
        numBluePots = connection.execute(sqlalchemy.text("SELECT num_blue_potions FROM global_inventory")).scalar()

    barrelsToDeliver = []

    if numRedPots < 10 and gold >= 100:
        gold -= 100
        barrelsToDeliver.append(
            {
                "sku": "SMALL_RED_BARREL",
                "quantity": 1,
            }
        )
    if numGreenPots < 10 and gold >= 100:
        gold -= 100
        barrelsToDeliver.append(
            {
                "sku": "SMALL_GREEN_BARREL",
                "quantity": 1,
            }
        )
    if numBluePots < 10 and gold >= 120:
        gold -= 120
        barrelsToDeliver.append(
            {
                "sku": "SMALL_BLUE_BARREL",
                "quantity": 1,
            }
        )
    return barrelsToDeliver