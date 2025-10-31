import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine

from app.data.session import Base
from app.data.models import *

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://appuser:apppass@postgres:5432/aiqfome")


async def init():
    print("📦 Criando tabelas do banco de dados...")
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print("✅ Banco e tabelas criados com sucesso!")


if __name__ == "__main__":
    asyncio.run(init())
