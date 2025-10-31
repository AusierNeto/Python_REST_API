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

class ProductBase(BaseModel):
    external_product_id: int
    title: str
    image_url: Optional[str]
    price: float
    rating_rate: Optional[float]
    rating_count: Optional[int]


class ProductSnapshot(ProductBase):
    id: int
    last_refreshed_at: datetime

    class Config:
        from_attributes = True


class FavoriteBase(BaseModel):
    external_product_id: int

class FavoriteResponse(BaseModel):
    external_product_id: int
    title: str
    image_url: Optional[str]
    price: float
    review: Optional[dict]
    favorited_at: datetime

    class Config:
        from_attributes = True

