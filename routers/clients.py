from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data.schemas import Client as ClientSchema
from data.models import Client
from data.session import get_db


router = APIRouter(prefix="/clients", tags=["clients"])

@router.get("/", response_model=list[ClientSchema])
async def get_clients(db: AsyncSession = Depends(get_db)):
    stmt = select(Client)
    result = await db.scalars(stmt)
    clients = result.all()

    return [ClientSchema(
        id=client.id,
        name=client.name,
        email=client.email,
        created_at=client.created_at,
        updated_at=client.updated_at
    ) for client in clients]

@router.post("/", response_model=ClientSchema)
async def create_client(data: ClientSchema, db: AsyncSession = Depends(get_db)):
    new_client = Client(
        name=data.name,
        email=data.email,
        created_at=data.created_at,
        updated_at=data.updated_at
    )
    db.add(new_client)
    await db.commit()
    await db.refresh(new_client)
    return new_client
