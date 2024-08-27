import json
from fastapi import HTTPException
from daos.domains.mysqldb.db import ServiceDB
from daos.models.inventories import Inventory
from typing import Mapping, Dict, Optional, Any
from uuid import UUID

class InventoryDAO:
    def __init__(self, connection: ServiceDB) -> None:
        self.servicedb = connection
    
    def get_inventory(self, inventory_id: UUID, data: Dict[str, Any]) -> Inventory | None:
        query = "SELECT * FROM inventories WHERE uuid = %s"
        cursor = self.servicedb.get_cursor()

        try: 
            cursor.execute(query, (inventory_id, data))
            result = cursor.fetchone()
        except Exception as e:
            print(f"[InventoryDAO] A DB error occurred: {e}")
            raise e
        finally:
            cursor.close()
        return self._unmarshal_inventory(result)

    def get_inventory_item(self, inventory_id: UUID, item_name: str) -> Optional[Dict[str, Any]]:
        query = "SELECT data FROM inventories WHERE uuid = %s"
        cursor = self.servicedb.get_cursor()

        try:
            cursor.execute(query, (inventory_id,))
            result = cursor.fetchone()
            if result:
                inventory_data = result[0]  # Assuming the `data` column is JSON
                items = json.loads(inventory_data)
                return items.get(item_name, None)
        except Exception as e:
            print(f"[InventoryDAO] A DB error occurred: {e}")
            raise e
        finally:
            cursor.close()
        return None

    def create_inventory(self, inventory: Inventory) -> Inventory:
        query = "INSERT INTO inventories (uuid, user_uuid, data) VALUES (%s, %s, %s)"
        cursor = self.servicedb.get_cursor()

        try:
            cursor.execute(query, (inventory.uuid, inventory.user_uuid, json.dumps(inventory.data)))
            self.servicedb.commit()
        except Exception as e:
            self.servicedb.rollback()
            print(f"[InventoryDAO] A DB error occurred: {e}")
            raise e
        finally:
            cursor.close()
        return self.get_inventory(inventory.uuid)

    def update_inventory(self, inventory_id: UUID, data: Dict[str, Any]) -> Inventory | None:
        query = "UPDATE inventories SET data = %s WHERE uuid = %s"
        cursor = self.servicedb.get_cursor()
        
        try:
            cursor.execute(query, (data, inventory_id))
            self.servicedb.commit()
        except Exception as e:
            self.servicedb.rollback()
            print(f"[InventoryDAO] A DB error occurred: {e}")
            raise e
        finally:
            cursor.close()
        return self.get_inventory(inventory_id)
        
    def add_item(self, inventory_id: UUID, item_name: str, quantity: int) -> Inventory | None:
        query = "SELECT data FROM inventories WHERE uuid = %s"
        cursor = self.servicedb.get_cursor()

        try:
            cursor.execute(query, (inventory_id,))
            result = cursor.fetchone()
            if result:
                inventory_data = result[0]  # Assuming the `data` column is JSON
                items = json.loads(inventory_data)
                if item_name in items:
                    items[item_name] += quantity
                else:
                    items[item_name] = quantity
                
                update_query = "UPDATE inventories SET data = %s WHERE uuid = %s"
                cursor.execute(update_query, (json.dumps(items), inventory_id))
                self.servicedb.commit()
                return self.get_inventory(inventory_id)
        except Exception as e:
            self.servicedb.rollback()
            print(f"[InventoryDAO] A DB error occurred: {e}")
            raise e
        finally:
            cursor.close()
        return None
    
    def delete_item(self, inventory_id: UUID, item_name: str, quantity: int) -> Inventory | None:
        query = "SELECT data FROM inventories WHERE uuid = %s"
        cursor = self.servicedb.get_cursor()

        try:
            cursor.execute(query, (inventory_id,))
            result = cursor.fetchone()
            if result:
                inventory_data = result[0]  # Assuming the `data` column is JSON
                items = json.loads(inventory_data)
                
                if item_name in items:
                    current_quantity = items[item_name]
                    
                    if quantity >= current_quantity:
                        # Remove item if quantity to delete is greater than or equal to available quantity
                        del items[item_name]
                    else:
                        # Reduce item quantity
                        items[item_name] -= quantity
                    
                    # Update the database
                    update_query = "UPDATE inventories SET data = %s WHERE uuid = %s"
                    cursor.execute(update_query, (json.dumps(items), inventory_id))
                    self.servicedb.commit()
                    return self.get_inventory(inventory_id)
                else:
                    raise HTTPException(status_code=404, detail="Item not found")
        except Exception as e:
            self.servicedb.rollback()
            print(f"[InventoryDAO] A DB error occurred: {e}")
            raise e
        finally:
            cursor.close()
        return None

    def delete_inventory(self, inventory_id: UUID) -> bool:
        query = "DELETE FROM inventories WHERE uuid = %s"
        cursor = self.servicedb.get_cursor()
        affected_rows = 0

        try:
            cursor.execute(query, (inventory_id,))
            self.servicedb.commit()
            affected_rows = cursor.rowcount
        except Exception as e:
            self.servicedb.rollback()
            print(f"[InventoryDAO] A DB error occurred: {e}")
            raise e
        finally:
            cursor.close()
        return affected_rows > 0

    def _unmarshal_inventory(self, db_record: Mapping | None) -> Inventory | None:
        if not db_record:
            return None
        return Inventory(**db_record)





