from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from datetime import datetime


Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(String, default=datetime.now().isoformat())
    updated_at = Column(String, default=datetime.now().isoformat())
