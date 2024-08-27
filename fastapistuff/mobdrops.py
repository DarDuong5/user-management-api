import random
import json
from enum import Enum
from fastapi import HTTPException
from typing import Dict, Any
from daos.domains.mysqldb.inventory_dao import InventoryDAO

class Mob(str, Enum):
    ladybug = "ladybug"
    rhino_beetle = "rhino beetle"
    spider = "spider"
    werewolf = "werewolf"

MobsDict = Dict[str, Any]

class LootHandler:
    def __init__(self, json_file: str, inventory_dao: InventoryDAO):
        self.json_file: str = json_file
        self.inventory_dao: InventoryDAO = inventory_dao
        self.mobs_dict: MobsDict = self._load_json()

    def _load_json(self):
        with open(self.json_file, 'r') as file:
            return json.load(file)
    
    def generate_loot(self, mob: Mob): 
        if mob.value not in self.mobs_dict:
            raise HTTPException(status_code=404, detail="mob not found")
        
        loot_table = self.mobs_dict[mob.value]['drops']
        loot_items = []

        for drop in loot_table:
            item_type = "item" if "item" in drop else "currency"
            item_name = drop.get("item") or drop.get("currency")
            drop_rate = drop["drop_rate"]
        
            if random.randint(1, 100) <= drop_rate:
                min_quantity = drop["min_quantity"]
                max_quantity = drop["max_quantity"]

                quantity = random.randint(min_quantity, max_quantity)
                
                if item_type == "item":
                    inventory.add_item(item_name, quantity)
                elif item_type == "currency":
                    inventory.add_currency(quantity)

                loot_items.append({"type": item_type, "name": item_name, "quantity": quantity})
        
        return loot_items