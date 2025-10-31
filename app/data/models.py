from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint, func
from datetime import datetime


Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(String, default=func.now(), onupdate=func.now())
    updated_at = Column(String, default=func.now(), onupdate=func.now())

class ProductSnapshot(Base):
    __tablename__ = "products_snapshot"

    id = Column(Integer, primary_key=True, index=True)
    external_product_id = Column(Integer, unique=True, nullable=False)
    title = Column(String, nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
    description = Column(String)
    category = Column(String)
    image_url = Column(String)
    rating_rate = Column(Numeric(3, 2))
    rating_count = Column(Integer)
    last_updated = Column(DateTime(timezone=True), server_default=func.now())

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    external_product_id = Column(Integer, nullable=False)
    product_snapshot_id = Column(Integer, ForeignKey("products_snapshot.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint("client_id", "external_product_id", name="client_product_index"),)

