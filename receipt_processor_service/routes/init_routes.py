from fastapi import APIRouter
from receipt_processor_service.routes.receipts import router as receipts_router

def create_router() -> APIRouter:
    router = APIRouter()

    router.include_router(receipts_router)

    return router

def get_api_router() -> APIRouter:
    return create_router()