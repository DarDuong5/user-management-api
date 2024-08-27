# Just in case I need it


# | class Item(BaseModel):
#     name: str
#     quantity: int
#     description: str | None = None

# class Inventory:
#     def __init__(self):
#         self.items: Dict[str, Item] = {}

#     def get(self, item: str) -> int:
#         if item not in self.items:
#             return 0
#         return self.items[item].quantity
    
#     def get_inv(self) -> List[Item]:
#         return self.items.values()
    
#     def add_item(self, item: str, quantity: int):
#         if item in self.items:
#             self.items[item].quantity += quantity
#             return
#         self.items[item] = Item(name = item, quantity = quantity)
#         return

# class AddItemRequest(BaseModel):
#     item: str
#     quantity: int

# inv = Inventory()

    
# @app.get("/bss_items")
# def display_items():
#     return [item.dict() for item in inv.get_inv()]

# @app.post("/bss_items")
# def add_item(req: AddItemRequest):
#     inv.add_item(req.item, req.quantity)
#     return {"success" : True}


# class BssGear(BaseModel):
#     name: str 
#     description: Optional[str] = None #Equivalent to " ... | None = None"
#     price: float
#     tax: float | None = None

# @app.post("/gear")
# def create_item(item: BssGear):
#     item_dict = item.dict()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax" : price_with_tax})
#     return item_dict

# @app.put("/gear/{gear_id}")
# def create_item_with_put(gear_id : int, item: BssGear, q : str | None = None):
#     result = {"item_id" : gear_id, **item.dict()}
#     if q: 
#         result.update({"q" : q})
#     return result