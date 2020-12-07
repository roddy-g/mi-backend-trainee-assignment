from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.storage_connection import Base
from api import storage
from tests.fixtures.items import *
from tests.fixtures.items_stats import *
from tests.fixtures.item_stat_requests import *
from tests.fixtures.responses_data import *
from datetime import datetime, timedelta


SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/fixtures/test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def test_get_item():
    db = TestingSessionLocal()
    storage.add_item(db, test_item)
    location_id = storage.get_item(db, test_item).location_id
    assert location_id == test_item.location_id
    storage.clear_db(db)
    db.close()


def test_add_item():
    db = TestingSessionLocal()
    advert_id = storage.add_item(db, test_item).id
    assert advert_id == storage.get_item(db, test_item).id
    storage.clear_db(db)
    db.close()


def test_add_stats():
    db = TestingSessionLocal()
    storage.add_item(db, test_item)
    for stat in item_stats:
        storage.add_stats(db, stat)
    assert storage.get_item_stat(db, test_item_stat_request) == response_stat
    storage.clear_db(db)
    db.close()


def test_get_item_stat():
    db = TestingSessionLocal()
    storage.clear_db(db)
    assert storage.get_item_stat(db, test_item_stat_request) is None
    storage.add_item(db, test_item)
    for stat in item_stats:
        storage.add_stats(db, stat)
    assert storage.get_item_stat(db, test_item_stat_request) == response_stat
    storage.clear_db(db)
    db.close()


def test_get_date_some_days_ago():
    days_delta = 2
    today = datetime.today()
    date_delta_days_ago = today - timedelta(days=2)
    assert storage.get_date_some_days_ago(days_delta).date() == date_delta_days_ago.date()


def test_get_item_by_id():
    db = TestingSessionLocal()
    item_id = storage.add_item(db, test_item).id
    item_from_db = storage.get_item(db, test_item)
    assert item_from_db.phrase == test_item.phrase
    assert item_from_db.location_id == test_item.location_id
    storage.clear_db(db)
    db.close()


def test_clear_db():
    db = TestingSessionLocal()
    storage.add_item(db, test_item)
    storage.add_item(db, test_item_1)
    for stat in item_stats:
        storage.add_stats(db, stat)
    storage.clear_db(db)
    assert storage.get_item(db, test_item) is None
    assert storage.get_item_stat(db, test_item_stat_request) is None
    db.close()
