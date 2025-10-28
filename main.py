from fastapi import FastAPI

from routers.clients import router as clients_router

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

app.include_router(clients_router)
