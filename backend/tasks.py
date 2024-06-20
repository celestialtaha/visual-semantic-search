import torch
from qdrant_client.models import PointStruct
from qdrant_client import AsyncQdrantClient
from PIL import Image
from io import BytesIO
import asyncio
import aiohttp

from celery_config import celery_app
from src.models import CLIPModelSingleton
from src.qdrant_agent import QdrantClientSingleton


async def download_image(image_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            response.raise_for_status()
            image_bytes = await response.read()
            image = Image.open(BytesIO(image_bytes))
            return image


async def get_existing_ids(client: AsyncQdrantClient):
    existing_ids = set()
    offset = 0
    limit = 100
    while True:
        response = await client.scroll(
            collection_name="products",
            scroll_filter=None,
            with_payload=True,
            with_vectors=False,
            limit=limit,
            offset=offset,
        )
        if not response[1]:
            break
        existing_ids.update(point.id for point in response[0])
        offset += limit
    return existing_ids


@celery_app.task(bind=True)
def encode_and_store_products(self, products):
    asyncio.run(_encode_and_store_products(self, products))


async def _encode_and_store_products(self, products):
    self.update_state(
        state="PROGRESS",
        meta={
            "current": 0,
            "total": 0,
            "status": "Loading/Downloading the encoding model",
        },
    )
    model = CLIPModelSingleton.get_model()
    processor = CLIPModelSingleton.get_processor()

    client = QdrantClientSingleton.get_client()

    existing_ids = await get_existing_ids(client)
    products_to_process = [
        product for product in products if product["id"] not in existing_ids
    ]

    total = len(products_to_process)

    for idx, product in enumerate(products_to_process):
        self.update_state(
            state="PROGRESS",
            meta={"current": idx, "total": total, "status": "Downloading images"},
        )

        combined_features = []
        for image_url in product.get("images", []):
            image = await download_image(image_url)
            image_features = processor(images=image, return_tensors="pt").pixel_values
            with torch.no_grad():
                image_features = model.get_image_features(image_features)
            combined_features.append(image_features)

        if combined_features:
            vector = (
                torch.mean(torch.stack(combined_features), dim=0).flatten().tolist()
            )

            self.update_state(
                state="PROGRESS",
                meta={"current": idx, "total": total, "status": "Storing in Qdrant"},
            )
            point = PointStruct(
                id=product["id"],
                vector=vector,
                payload={
                    "title": product["name"],
                    "description": product["description"],
                    "category": product.get("category_name"),
                    "price": product["current_price"],
                    "sizes": product["sizes"],
                    "status": product["status"],
                },
            )

            await client.upsert(collection_name="products", points=[point])

    return {"status": "success", "processed_products": total}
