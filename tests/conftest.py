import pytest
from tests.test_storage import TestingSessionLocal
from app.storage import clear_db

@pytest.fixture
def db():
    db = TestingSessionLocal()
    yield db
    clear_db(db)
    db.close()