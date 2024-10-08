import sqlalchemy
from src import database as db
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import math

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/audit")
def get_inventory():
    """ """
    with db.engine.begin() as connection:
        gold = connection.execute(sqlalchemy.text("SELECT gold FROM global_inventory")).scalar()
        numRed = connection.execute(sqlalchemy.text("SELECT num_red_potions FROM global_inventory")).scalar()
        numGreen = connection.execute(sqlalchemy.text("SELECT num_green_potions FROM global_inventory")).scalar()
        numBlue = connection.execute(sqlalchemy.text("SELECT num_blue_potions FROM global_inventory")).scalar()
        redMl = connection.execute(sqlalchemy.text("SELECT num_red_ml FROM global_inventory")).scalar()
        greenMl = connection.execute(sqlalchemy.text("SELECT num_green_ml FROM global_inventory")).scalar()
        blueMl = connection.execute(sqlalchemy.text("SELECT num_blue_ml FROM global_inventory")).scalar()
        totalPots =  numRed + numGreen + numBlue
        totalMl = redMl + greenMl + blueMl

    
    return {"number_of_potions": totalPots, "ml_in_barrels": totalMl, "gold": gold}

# Gets called once a day
@router.post("/plan")
def get_capacity_plan():
    """ 
    Start with 1 capacity for 50 potions and 1 capacity for 10000 ml of potion. Each additional 
    capacity unit costs 1000 gold.
    """

    return {
        "potion_capacity": 0,
        "ml_capacity": 0
        }

class CapacityPurchase(BaseModel):
    potion_capacity: int
    ml_capacity: int

# Gets called once a day
@router.post("/deliver/{order_id}")
def deliver_capacity_plan(capacity_purchase : CapacityPurchase, order_id: int):
    """ 
    Start with 1 capacity for 50 potions and 1 capacity for 10000 ml of potion. Each additional 
    capacity unit costs 1000 gold.
    """

    return "OK"
