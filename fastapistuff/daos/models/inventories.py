from pydantic import BaseModel, Field
from typing import Dict, Any
from uuid import UUID

class InventoryBase(BaseModel):
    uuid: UUID

class CreateInventory(InventoryBase):
    user_uuid: str

class GetInventory(InventoryBase):
    user_uuid: str

class Inventory(InventoryBase):
    uuid: UUID
    user_uuid: str
    data: Dict[str, Any] = Field(default_factory=dict)