from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.db import Base
from api import database_functions
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
    database_functions.add_item(db, test_item)
    location_id = database_functions.get_item(db, test_item).location_id
    assert location_id == test_item.location_id
    database_functions.clear_db(db)
    db.close()


def test_add_item():
    db = TestingSessionLocal()
    advert_id = database_functions.add_item(db, test_item).id
    assert advert_id == database_functions.get_item(db, test_item).id
    database_functions.clear_db(db)
    db.close()


def test_add_stats():
    db = TestingSessionLocal()
    database_functions.add_item(db, test_item)
    for stat in item_stats:
        database_functions.add_stats(db, stat)
    assert database_functions.get_item_stat(db, test_item_stat_request) == response_stat
    database_functions.clear_db(db)
    db.close()


def test_get_item_stat():
    db = TestingSessionLocal()
    database_functions.clear_db(db)
    assert database_functions.get_item_stat(db, test_item_stat_request) is None
    database_functions.add_item(db, test_item)
    for stat in item_stats:
        database_functions.add_stats(db, stat)
    assert database_functions.get_item_stat(db, test_item_stat_request) == response_stat
    database_functions.clear_db(db)
    db.close()


def test_get_date_some_days_ago():
    days_delta = 2
    today = datetime.today()
    date_delta_days_ago = today - timedelta(days=2)
    assert database_functions.get_date_some_days_ago(days_delta).date() == date_delta_days_ago.date()


def test_get_item_by_id():
    db = TestingSessionLocal()
    item_id = database_functions.add_item(db, test_item).id
    item_from_db = database_functions.get_item(db, test_item)
    assert item_from_db.phrase == test_item.phrase
    assert item_from_db.location_id == test_item.location_id
    database_functions.clear_db(db)
    db.close()


def test_clear_db():
    db = TestingSessionLocal()
    database_functions.add_item(db, test_item)
    database_functions.add_item(db, test_item_1)
    for stat in item_stats:
        database_functions.add_stats(db, stat)
    database_functions.clear_db(db)
    assert database_functions.get_item(db, test_item) is None
    assert database_functions.get_item_stat(db, test_item_stat_request) is None
    db.close()
