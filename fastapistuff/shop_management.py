from fastapi import HTTPException
import json

class Shop:
    def __init__(self, json_file):
        self.json_file = json_file
        self.data = self._load_json()
        
    def _load_json(self):
        with open(self.json_file, 'r') as file:
            return json.load(file)
        
    def purchase_item(self, item_category : str, item_name : str, inventory : Inventory):
        if item_category not in self.data:
            raise HTTPException(status_code=404, detail="item category not found")

        if item_name not in self.data[item_category]:
            raise HTTPException(status_code=404, detail="item not found")
        
        item_price = self.data[item_category][item_name]['price']

        if inventory.currency["honey"] < item_price:
            raise HTTPException(status_code=400, detail="not enough honey for this item")
        
        if 'items' in self.data[item_category][item_name]:
            item_requirements = self.data[item_category][item_name]['items']
            for req_item, req_quantity in item_requirements.items():
                if inventory.items.get(req_item, 0) < req_quantity:
                    raise HTTPException(status_code=400, detail=f"not enough {req_item} to craft {item_name}")
            
            for req_item, req_quantity in item_requirements.items():
                inventory.remove_item(req_item, req_quantity)
            
        inventory.remove_currency(item_price)
        inventory.add_item(item_name, 1)
        return {"message" : f"purchased {item_name}"}
