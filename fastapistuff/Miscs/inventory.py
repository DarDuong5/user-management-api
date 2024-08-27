from fastapi import HTTPException

class Inventory:
    def __init__(self):
        self.honey = 2000
        self.items = {
            "basic egg" : 1,
            "pouch" : 1,
            "scooper" : 1
        }

    def get_all(self): 
        return {"inventory" : self.items, "currency" : self.honey} 
    
    def get_inventory(self):
        return {"inventory" : self.items}
    
    def get_item(self, item : str):
        if item in self.items:
            return {"item found" : self.items[item]}
        raise HTTPException(status_code=404, detail="item not found")
    
    def add_item(self, item : str, quantity : int):
        if item in self.items:
            self.items[item] += quantity
        else:
            self.items[item] = quantity
        return {"item added" : {self.items[item]}, "inventory" : self.items}

    def remove_item(self, item : str, quantity : int):
        if item in self.items:
            if self.items[item] >= quantity:
                self.items[item] -= quantity
                if self.items[item] == 0:
                    del self.items[item]
                return {"item removed" : {item : self.items.get(item, 0)}}
        else:
            raise HTTPException(status_code=400, detail="not enough item(s) to remove")
        raise HTTPException(status_code=404, detail="item not found")
    
    def get_currency(self):
        return {"currency" : self.honey}
    
    def add_currency(self, amount : int):
        self.honey += amount
        return self.get_currency()

    def remove_currency(self, amount : int): 
        self.honey -= amount
        return self.get_currency()          


