import json
from fastapi import HTTPException
from inventory import Inventory

class Blender:
    def __init__(self, json_file):
        self.json_file = json_file
        self.recipes = self._load_json()

    def _load_json(self):
        with open(self.json_file, 'r') as file:
            return json.load(file)

    def blend_item(self, item_name, inventory : Inventory):
        if item_name not in self.recipes:
            raise HTTPException(status_code=404, detail="Item not found in blender recipes")
        
        recipe = self.recipes[item_name]

        for ingredient in recipe:
            item = ingredient['item']
            quantity = ingredient['quantity']
            if inventory.items.get(item, 0) < quantity:
                raise HTTPException(status_code=400, detail=f"Not enough {item} to craft {item_name}")

        for ingredient in recipe:
            item = ingredient['item']
            quantity = ingredient['quantity']
            inventory.remove_item(item, quantity)
        
        inventory.add_item(item_name, 1)
        return {"message": f"Crafted {item_name}"}
