from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

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
    try:
        await db.commit()
        await db.refresh(new_client)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Client with this email already exists.")
    
    return new_client

@router.put("/{client_id}", response_model=ClientSchema)
async def put_client(data: ClientSchema, db: AsyncSession = Depends(get_db)):
    pass

@router.patch("/{client_id}", response_model=ClientSchema)
async def patch_client(data: ClientSchema, db: AsyncSession = Depends(get_db)):
    pass

@router.delete("/{client_id}", response_model=dict)
async def delete_client(client_id: int, db: AsyncSession = Depends(get_db)):
    pass