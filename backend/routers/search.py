import torch
from fastapi import APIRouter, Query

from src.models import CLIPModelSingleton
from src.qdrant_agent import QdrantClientSingleton


router = APIRouter()

qdrant_client = QdrantClientSingleton.get_client()

@router.post("/query")
async def search(query: str, category: str = Query(None), price: int = Query(None)):
    model = CLIPModelSingleton.get_model()
    processor = CLIPModelSingleton.get_processor()
    
    text_features = processor(text=query, return_tensors="pt")
    with torch.no_grad():
        text_features = model.get_text_features(**text_features).flatten().tolist()

    filter_conditions = []
    
    if category:
        filter_conditions.append({"key": "category", "match": {"value": category}})
    if price is not None:
        filter_conditions.append({"key": "price", "range": {"lt": price}})
    
    search_result = await qdrant_client.search(
        collection_name="products",
        query_vector=text_features,
        limit=20,
        query_filter={"must": filter_conditions} if filter_conditions else None
    )
    
    return search_result
