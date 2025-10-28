from datetime import datetime
from pydantic import BaseModel


class Client(BaseModel):
    name: str
    email: str
    created_at: str | None = datetime.now().isoformat()
    updated_at: str | None = datetime.now().isoformat()

class Product(BaseModel):
    title: str
    price: float
    description: int
    category: str
    image: str
    rating: dict | None = None
