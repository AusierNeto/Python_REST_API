import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from ..data.models import ProductSnapshot

FAKESTORE_URL = "https://fakestoreapi.com/products"

async def fetch_product_from_api(product_id: int) -> dict:
    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.get(f"{FAKESTORE_URL}/{product_id}")
        if resp.status_code != 200:
            return None
        return resp.json()
    
async def get_or_create_product_snapshot(db: AsyncSession, product_id: int) -> ProductSnapshot:
    stmt = select(ProductSnapshot).where(ProductSnapshot.external_product_id == product_id)
    result = await db.scalars(stmt)
    snapshot = result.first()

    if snapshot and snapshot.last_refreshed_at > datetime.now(datetime.timezone.utc) - timedelta(hours=1):
        return snapshot

    data = await fetch_product_from_api(product_id)
    if not data:
        return None

    if snapshot:
        snapshot.title = data["title"]
        snapshot.image_url = data["image"]
        snapshot.price = data["price"]
        snapshot.rating_rate = data["rating"]["rate"]
        snapshot.rating_count = data["rating"]["count"]
        snapshot.last_refreshed_at = datetime.utcnow()
    else:
        snapshot = ProductSnapshot(
            external_product_id=data["id"],
            title=data["title"],
            image_url=data["image"],
            price=data["price"],
            rating_rate=data["rating"]["rate"],
            rating_count=data["rating"]["count"],
        )
        db.add(snapshot)

    await db.commit()
    await db.refresh(snapshot)
    return snapshot


