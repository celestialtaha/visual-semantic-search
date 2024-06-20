from fastapi import APIRouter
from . import products, tasks, search

router = APIRouter()
router.include_router(products.router, prefix="/products", tags=["products"])
router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
router.include_router(search.router, prefix="/search", tags=["search"])
