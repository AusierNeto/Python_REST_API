from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from data.models import Base


DATABASE_URL = "postgresql+psycopg2://ausier:ausier@localhost:5432/mglu_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

