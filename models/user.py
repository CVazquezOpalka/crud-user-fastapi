from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    password: str


class UpdateUser(BaseModel):
    name: str
    email: str
    password: str
