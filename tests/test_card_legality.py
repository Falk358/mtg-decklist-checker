import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def test_client():
    client = TestClient(app, raise_server_exceptions=True)
    yield client


def test_cardname_endpoint(test_client: TestClient):
    response = test_client.post(url="/cardlegality", json={"card_name": "Sol Ring"})
    print(response.json())
    assert response.status_code == 200
