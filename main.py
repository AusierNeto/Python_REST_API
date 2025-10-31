from fastapi import FastAPI
from routers.clients import router as clients_router
from routers.favorites import router as favorites_router


app = FastAPI()

app.include_router(clients_router)
app.include_router(favorites_router)
