from pydantic import BaseModel
from datetime import datetime


class Item(BaseModel):
    phrase: str
    location_id: int

    class Config:
        orm_mode = True


class ItemStats(BaseModel):
    item_id: int
    items_quantity: int
    timestamp: datetime

    class Config:
        orm_mode = True


class ItemStatRequest(BaseModel):
    item_id: int
    interval: int

    class Config:
        orm_mode = True
