from fastapi import HTTPException
from typing import Dict, Any
from daos.models.inventories import Inventory, CreateInventory, GetInventory
from daos.domains.mysqldb.inventory_dao import InventoryDAO
from pymysql.err import IntegrityError

class InventoryHandler:
    def __init__(self, inventory_dao: InventoryDAO) -> None: 
        self.inventory_dao = inventory_dao

    async def create_inventory(self, req: CreateInventory) -> Inventory | None:
        try:
            created_inventory = self.inventory_dao.create_inventory(req.user_uuid)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while creating the inventory: {e}")
        
        return created_inventory

    async def get_inventory(self, req: GetInventory) -> Inventory | None:
        try:
            fetched_inventory = self.inventory_dao.get_inventory(req.user_uuid)
        except IntegrityError:
            raise HTTPException(status_code=404, detail="Inventory does not exist.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while getting the inventory: {e}")
        
        return fetched_inventory

