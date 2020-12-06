from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.database_connection import Base, get_db
from api.main import app
from api import database_functions
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


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_path_add():
    db = TestingSessionLocal()
    database_functions.clear_db(db)
    db.close()
    response = client.post(
        "/add",
        json={'phrase': test_item.phrase,
              'location_id': 'string type of location'}
    )
    assert response.status_code == 422
    response = client.post(
        "/add",
        json={'phrase': test_item.phrase,
              'location_id': test_item.location_id}
    )
    assert response.status_code == 200
    assert response.json()['message'] == response_success_registered
    response = client.post(
        "/add",
        json={'phrase': test_item.phrase,
              'location_id': test_item.location_id}
    )
    assert response.status_code == 400
    assert response.json()['detail'] == response_already_registered
    db = TestingSessionLocal()
    database_functions.clear_db(db)
    db.close()


def test_path_stat():
    db = TestingSessionLocal()
    database_functions.clear_db(db)
    db.close()
    response = client.post(
        "/stat",
        json={'item_id': test_item_stat_request.item_id,
              'interval': test_item_stat_request.interval}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'No such advert'}
    db = TestingSessionLocal()
    database_functions.add_item(db, test_item)
    for stat in item_stats:
        database_functions.add_stats(db, stat)
    db.close()
    response = client.post(
        "/stat",
        json={'item_id': test_item_stat_request.item_id,
              'interval': test_item_stat_request.interval}
    )
    assert response.status_code == 200
    print(response.json())
    assert response.json() == response_stat
    db = TestingSessionLocal()
    database_functions.clear_db(db)
    db.close()
    response = client.post(
        "/stat",
        json={'item_id': test_item_stat_request.item_id,
              'interval': 'string'}
    )
    assert response.status_code == 422



