import asyncio

from data.session import engine, Base
from data.models import *

async def init_db():
    async with engine.begin() as conn:
        print("Criando tabelas no banco de dados...")
        await conn.run_sync(Base.metadata.create_all)
        print("Banco e tabelas criados com sucesso!")

if __name__ == "__main__":
    asyncio.run(init_db())
