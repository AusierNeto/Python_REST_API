from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ClientBase(BaseModel):
    id: Optional[int]
    name: str
    email: str
    created_at: Optional[str]
    updated_at: Optional[str]

class ClientCreate(BaseModel):
    name: Optional[str]
    email: Optional[str]

class Product(BaseModel):
    title: str
    price: float
    description: int
    category: str
    image: str
    rating: Optional[dict]
