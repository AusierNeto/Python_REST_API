import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv
from .models import Base


load_dotenv()

engine = create_async_engine(os.environ.get("DATABASE_URL"), echo=False)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

