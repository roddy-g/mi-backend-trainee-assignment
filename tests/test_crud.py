from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.db import Base
from api import crud
from api import schemas, models
from tests.fixtures.items import test_item
from tests.fixtures.items_stats import item_stats
from tests.fixtures.item_stat_requests import test_item_stat_request
from tests.fixtures.responses_data import *

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/fixtures/test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def test_get_item():
    db = TestingSessionLocal()
    crud.add_item(db, test_item)
    location_id = crud.get_item(db, test_item).location_id
    assert location_id == test_item.location_id
    crud.clear_db(db)
    db.close()


def test_add_item():
    db = TestingSessionLocal()
    advert_id = crud.add_item(db, test_item).id
    assert advert_id == crud.get_item(db, test_item).id
    crud.clear_db(db)
    db.close()


def test_add_stats():
    db = TestingSessionLocal()
    crud.add_item(db, test_item)
    for stat in item_stats:
        crud.add_stats(db, stat)
    assert crud.get_item_stat(db, test_item_stat_request) == response_stat
    crud.clear_db(db)
    db.close()


def test_get_item_stat():
    db = TestingSessionLocal()
    crud.add_item(db, test_item)
    for stat in item_stats:
        crud.add_stats(db, stat)
    assert crud.get_item_stat(db, test_item_stat_request) == response_stat
    crud.clear_db(db)
    db.close()



