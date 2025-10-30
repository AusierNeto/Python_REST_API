import httpx

FAKESTORE_URL = "https://fakestoreapi.com/products"

async def fetch_product_from_api(product_id: int) -> dict:
    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.get(f"{FAKESTORE_URL}/{product_id}")
        if resp.status_code != 200:
            return None
        return resp.json()

async def fetch_products_from_api() -> dict:
    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.get(f"{FAKESTORE_URL}")
        if resp.status_code != 200:
            return None
        return resp.json()


if __name__ == "__main__":
    import asyncio

    print(asyncio.run(fetch_products_from_api()))
