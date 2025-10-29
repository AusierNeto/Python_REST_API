from fastapi import APIRouter, Depends
from data.schemas import Client as ClientSchema
from data.models import Client
from data.session import get_db


router = APIRouter(prefix="/clients", tags=["clients"])

@router.get("/")
async def get_clients(db=Depends(get_db)) -> list[ClientSchema]:
    clients = db.query(Client).all()
    return [ClientSchema(
        id=client.id,
        name=client.name,
        email=client.email,
        created_at=client.created_at,
        updated_at=client.updated_at
    ) for client in clients]

@router.post("/")
async def create_client(data:ClientSchema, db=Depends(get_db)):
    new_client = Client(
        name=data.name,
        email=data.email,
        created_at=data.created_at,
        updated_at=data.updated_at
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return {"message": "Client created", "client": data}

