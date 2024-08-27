from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    username: str

class CreateUser(UserBase):
    username: str

class UpdateUser(UserBase):
    uuid: UUID
    username: str

class DeleteUser(UserBase):
    uuid: UUID
    username: str

class User(UserBase):
    uuid: UUID
    username: str
    created_at: datetime