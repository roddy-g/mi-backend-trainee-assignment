from api import main
from fastapi.testclient import TestClient

client = TestClient(main.app)


def test_register():
    response = client.post(
        "/add",
        json={'phrase': 'eee', 'location_id': 637640}
    )
    response = client.post(
        "/add",
        json={'phrase': 'eee', 'location_id': 637640}
    )
    assert response.status_code == 400
