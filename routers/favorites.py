from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from data.session import get_db
from data.models import Favorite
from data.schemas import FavoriteBase, FavoriteResponse
from services.products import get_or_create_product_snapshot


router = APIRouter(prefix="/clients/{client_id}/favorites", tags=["Favorites"])

@router.post("/", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
async def add_favorite(client_id: int, data: FavoriteBase, db: AsyncSession = Depends(get_db)):
    stmt = select(Favorite).where(
        Favorite.client_id == client_id,
        Favorite.external_product_id == data.external_product_id
    )
    result = await db.scalars(stmt)
    if result.first():
        raise HTTPException(status_code=409, detail="Product already favorited by this client.")

    snapshot = await get_or_create_product_snapshot(db, data.external_product_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Product not found in external API.")

    favorite = Favorite(
        client_id=client_id,
        external_product_id=data.external_product_id,
        product_snapshot_id=snapshot.id
    )

    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)

    return FavoriteResponse(
        external_product_id=snapshot.external_product_id,
        title=snapshot.title,
        image_url=snapshot.image_url,
        price=float(snapshot.price),
        review={
            "rate": float(snapshot.rating_rate or 0),
            "count": snapshot.rating_count or 0
        },
        favorited_at=favorite.created_at
    )


@router.get("/", response_model=list[FavoriteResponse])
async def list_favorites(client_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Favorite).where(Favorite.client_id == client_id)
    favorites = (await db.scalars(stmt)).all()

    response = []
    for fav in favorites:
        snapshot = await db.get(type(fav).metadata.tables["products_snapshot"].mapper.class_, fav.product_snapshot_id)
        if not snapshot:
            continue
        response.append(FavoriteResponse(
            external_product_id=snapshot.external_product_id,
            title=snapshot.title,
            image_url=snapshot.image_url,
            price=float(snapshot.price),
            review={
                "rate": float(snapshot.rating_rate or 0),
                "count": snapshot.rating_count or 0
            },
            favorited_at=fav.created_at
        ))

    return response


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_favorite(client_id: int, product_id: int, db: AsyncSession = Depends(get_db)):
    stmt = delete(Favorite).where(
        Favorite.client_id == client_id,
        Favorite.external_product_id == product_id
    )
    result = await db.execute(stmt)

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Favorite not found.")

    await db.commit()
    return

