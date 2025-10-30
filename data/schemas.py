from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Client(BaseModel):
    name: str
    email: str
    created_at: Optional[str]
    updated_at: Optional[str]

class Product(BaseModel):
    title: str
    price: float
    description: int
    category: str
    image: str
    rating: Optional[dict]
