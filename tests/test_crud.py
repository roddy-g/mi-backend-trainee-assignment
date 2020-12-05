from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.db import Base
from api import database_functions
from tests.fixtures.items import test_item
from tests.fixtures.items_stats import item_stats
from tests.fixtures.item_stat_requests import test_item_stat_request
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



