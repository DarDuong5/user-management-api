from fastapi import FastAPI, HTTPException, Query, Depends
from daos.domains.mysqldb.db import ServiceDB
from daos.domains.mysqldb.user_dao import UserDAO
from daos.handlers.inventory_handler import InventoryHandler
from daos.handlers.user_handler import UserHandler
from daos.models.inventories import Inventory, CreateInventory, GetInventory
from mobdrops import Mob, LootHandler 

app = FastAPI()
db = ServiceDB()

def get_user_dao(db: ServiceDB = Depends(db)):
    return UserDAO()(connection=db)

def get_user_handler(dao: UserDAO = Depends(get_user_dao)):
    return UserHandler()(user_dao=dao)

@app.get("/inventory/create")
def create_inventory(req: CreateInventory, inventory: InventoryHandler = Depends(get_user_handler)) -> Inventory:
    return inventory.create_inventory(req)

@app.get("/inventory")
def get_inventory(req: GetInventory, inventory: InventoryHandler = Depends(get_user_handler)) -> Inventory:
    return inventory.get_inventory(req)


#@app.post("/kill-mob")
#def kill_mob(mob_type : Mob = Query(..., description="choose the mob you want to defeat")):





