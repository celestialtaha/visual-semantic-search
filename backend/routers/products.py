from fastapi import APIRouter, BackgroundTasks
from qdrant_client.models import Distance, VectorParams

from tasks import encode_and_store_products
from src.qdrant_agent import QdrantClientSingleton
from src.utils import load_products

router = APIRouter()
qdrant_client = QdrantClientSingleton.get_client()


@router.post("/add")
async def add_products(background_tasks: BackgroundTasks):
    products = await load_products("products.json")
    collection_exists = await qdrant_client.collection_exists("products")
    if not collection_exists:
        await qdrant_client.create_collection(
            collection_name="products",
            vectors_config=VectorParams(size=512, distance=Distance.COSINE),
        )
    task = encode_and_store_products.delay(products)
    return {"message": "Products are being processed", "task_id": task.id}
