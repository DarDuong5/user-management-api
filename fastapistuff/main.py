from fastapi import FastAPI, HTTPException, Query, Depends
from daos.domains.mysqldb.db import ServiceDB
from daos.domains.mysqldb.user_dao import UserDAO
from daos.handlers.inventory_handler import InventoryHandler
from daos.handlers.user_handler import UserHandler
from daos.models.inventories import Inventory, CreateInventory, GetInventory
from mobdrops import Mob, LootHandler 

app = FastAPI()
# Dependency to get the database connection
def get_db() -> ServiceDB: # type: ignore
    db = ServiceDB()
    try:
        yield db
    finally:
        db.close()

def get_user_dao(db: ServiceDB = Depends(get_db)) -> UserDAO:
    return UserDAO(connection=db)

def get_inventory_dao(db: ServiceDB = Depends(get_db)) -> InventoryDAO:
    return InventoryDAO(connection=db)

def get_user_handler(dao: UserDAO = Depends(get_user_dao)) -> UserHandler:
    return UserHandler(user_dao=dao)

def get_inventory_handler(dao: InventoryDAO = Depends(get_inventory_dao)) -> InventoryHandler:
    return InventoryHandler(inventory_dao=dao)

@app.post("/user/create", response_model=User)
async def create_user(req: CreateUser, user_handler: UserHandler = Depends(get_user_handler)) -> User:
    return user_handler.create_user(req)



