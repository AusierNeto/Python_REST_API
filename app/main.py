from fastapi import FastAPI
from .routers.clients import router as clients_router
from .routers.favorites import router as favorites_router


app = FastAPI(
    title="Client Favorites API",
    description="API for managing clients and their favorite products with external product data integration.",
    version="0.1.0"
)


app.include_router(clients_router)
app.include_router(favorites_router)
