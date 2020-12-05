from sqlalchemy import Column, Integer, String, DateTime
from api.db import Base
from sqlalchemy.schema import UniqueConstraint


class Items(Base):
    __tablename__ = "items"

    UniqueConstraint('phrase', 'location_id')
    id = Column(Integer, primary_key=True)
    phrase = Column(String)
    location_id = Column(Integer)


class ItemsStats(Base):
    __tablename__ = "items_stats"

    id = Column(Integer, primary_key=True)
    phrase = Column(String)
    location_id = Column(Integer)
    advert_count = Column(Integer)
    timestamp = Column(DateTime)
