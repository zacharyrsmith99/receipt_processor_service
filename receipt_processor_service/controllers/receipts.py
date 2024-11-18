from typing import Dict
from uuid import uuid4
from receipt_processor_service.receipt_processor.receipt_model import Receipt

class ReceiptsController:
    def __init__(self):
        self._receipts: Dict[str, Dict] = {}
    
    def process_receipt(self, receipt: Receipt) -> str:
        try:
            receipt_id = str(uuid4())
            points = self._calculate_points(receipt)
            
            self._receipts[receipt_id] = {
                "receipt": receipt,
                "points": points
            }
            
            return receipt_id
        except Exception as e:
            raise ValueError(f"Failed to process receipt: ({str(e)})")
    
    def get_points(self, receipt_id: str) -> int:
        if receipt_id not in self._receipts:
            raise ValueError("Receipt not found!")
        
        return self._receipts[receipt_id]["points"]
    
    def _calculate_points(self, receipt: Receipt) -> int:
        points = 0
        
        # Points for retailer name
        points += sum(c.isalnum() for c in receipt.retailer)
        
        # Round dollar amount
        if receipt.total.endswith(".00"):
            points += 50
        
        # Multiple of 0.25
        total_float = float(receipt.total)
        if total_float % 0.25 == 0:
            points += 25
        
        # Pairs of items
        points += (len(receipt.items) // 2) * 5
        
        # Description length multiplier
        for item in receipt.items:
            trimmed_length = len(item.shortDescription.strip())
            if trimmed_length % 3 == 0:
                print(points)
                item_points = float(item.price) * 0.2
                points += int(item_points + 0.99)
                print(points)
        
        # Odd day points
        if receipt.purchaseDate.day % 2 == 1:
            points += 6
        
        # Time range points (2:00 PM to 4:00 PM)
        purchase_time = receipt.purchaseTime
        if (14 <= purchase_time.hour < 16) or (purchase_time.hour == 16 and purchase_time.minute == 0):
            points += 10
        
        return points