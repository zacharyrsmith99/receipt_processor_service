from pydantic import BaseModel, Field
from typing import List
from datetime import date, time

class Item(BaseModel):
    shortDescription: str = Field(
        ...,
        description="The Short Product Description for the item.",
        example="Mountain Dew 12PK",
        pattern=r"^[\w\s\-]+$"
    )
    price: str = Field(
        ...,
        description="The total price paid for this item.",
        example="6.49",
        pattern=r"^\d+\.\d{2}$"
    )

class Receipt(BaseModel):
    retailer: str = Field(
        ...,
        description="The name of the retailer or store the receipt is from.",
        example="M&M Corner Market",
        pattern=r"^[\w\s\-&]+$"
    )
    purchaseDate: date = Field(
        ...,
        description="The date of the purchase printed on the receipt.",
        example="2022-01-01"
    )
    purchaseTime: time = Field(
        ...,
        description="The time of the purchase printed on the receipt. 24-hour time expected.",
        example="13:01"
    )
    items: List[Item] = Field(
        ...,
        description="The items purchased on the receipt.",
        min_items=1
    )
    total: str = Field(
        ...,
        description="The total amount paid on the receipt.",
        example="6.49",
        pattern=r"^\d+\.\d{2}$"
    )