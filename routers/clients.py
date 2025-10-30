from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from data.schemas import ClientBase, ClientCreate
from data.models import Client
from data.session import get_db


router = APIRouter(prefix="/clients", tags=["clients"])

@router.get("/", response_model=list[ClientBase])
async def get_clients(db: AsyncSession = Depends(get_db)):
    stmt = select(Client)
    result = await db.scalars(stmt)
    clients = result.all()

    return [ClientBase(
        id=client.id,
        name=client.name,
        email=client.email,
        created_at=client.created_at,
        updated_at=client.updated_at
    ) for client in clients]

@router.get("/{client_id}", response_model=ClientBase)
async def get_client_by_id(client_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Client).where(Client.id == client_id)
    result = await db.scalars(stmt)
    client = result.first()

    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found.")
    
    return client

@router.post("/", response_model=ClientBase)
async def create_client(data: ClientCreate, db: AsyncSession = Depends(get_db)):
    new_client = Client(
        name=data.name,
        email=data.email
    )
    
    db.add(new_client)
    try:
        await db.commit()
        await db.refresh(new_client)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Client with this email already exists.")
    
    return new_client

@router.put("/{client_id}", response_model=ClientBase)
async def put_client(client_id: int, data: ClientCreate, db: AsyncSession = Depends(get_db)):
    """
    Substitui completamente os dados de um cliente.
    Requer todos os campos obrigatórios (PUT = substituição total).
    """
    stmt = select(Client).where(Client.id == client_id)
    result = await db.scalars(stmt)
    client = result.first()

    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found.")

    client.name = data.name
    client.email = data.email

    try:
        await db.commit()
        await db.refresh(client)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already in use by another client.")

    return client

@router.patch("/{client_id}", response_model=ClientBase)
async def patch_client(client_id: int, data: ClientCreate, db: AsyncSession = Depends(get_db)):
    """
    Atualiza parcialmente os dados de um cliente.
    Somente os campos enviados serão modificados.
    """
    stmt = select(Client).where(Client.id == client_id)
    result = await db.scalars(stmt)
    client = result.first()

    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found.")

    # Atualiza apenas os campos enviados (PATCH = atualização parcial)
    update_fields = data.model_dump(exclude_unset=True)

    for field, value in update_fields.items():
        setattr(client, field, value)

    try:
        await db.commit()
        await db.refresh(client)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already in use by another client.")

    return client

@router.delete("/{client_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_client(client_id: int, db: AsyncSession = Depends(get_db)):
    """
    Remove um cliente pelo ID.
    """
    stmt = select(Client).where(Client.id == client_id)
    result = await db.scalars(stmt)
    client = result.first()

    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found.")

    await db.delete(client)
    await db.commit()

    return {"message": f"Client with ID {client_id} deleted successfully."}

