from fastapi import APIRouter, HTTPException
from receipt_processor_service.receipt_processor.receipt_model import Receipt
from receipt_processor_service.controllers.receipts import ReceiptsController
from pydantic import BaseModel

router = APIRouter()
receipts_controller = ReceiptsController()


class ReceiptResponse(BaseModel):
    id: str

class PointsResponse(BaseModel):
    points: int

@router.post("/receipts/process", response_model=ReceiptResponse)
async def process_receipt(receipt: Receipt):
    try:
        receipt_id = receipts_controller.process_receipt(receipt)
        return ReceiptResponse(id=receipt_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/receipts/{id}/points", response_model=PointsResponse)
async def get_points(id: str):
    try:
        points = receipts_controller.get_points(id)
        return PointsResponse(points=points)
    except ValueError as e:
        if str(e) == "Receipt not found!":
            raise HTTPException(status_code=404, detail="Receipt not found")
        
        raise HTTPException(status_code=400, detail=str(e))