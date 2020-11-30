from pydantic import BaseModel
from datetime import datetime


class Advert(BaseModel):
    phrase: str
    location_id: int

    class Config:
        orm_mode = True


class AdvertStats(Advert):
    advert_count: int
    timestamp: datetime

    class Config:
        orm_mode = True


class AdvertStatRequest(BaseModel):
    advert_id: int
    interval: int

    class Config:
        orm_mode = True
