import pytest
from fastapi.testclient import TestClient
from data-processing-pipeline.api import DATA_COLLECTED, app

@pytest.fixture
def client():
    # Provide a fresh TestClient for each test
    return TestClient(app)

def test_ping(client):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}

def test_data_no_key(client):
    response = client.get("/data")
    assert response.status_code == 401  # missing X-API-KEY

def test_data_with_key(client, monkeypatch):
    # monkeypatch the required API_KEY environment or the global var
    monkeypatch.setenv("API_KEY", "testkey")
    
    from data-processing-pipeline.api import REQUIRED_API_KEY
    
    
    # we must reassign because we read env at import time
    # if the code is using os.environ.get inside the file, you might need a refactor

    # Pre-load some data
    DATA_COLLECTED[:] = [{"created_at": "2023-01-01", "value": 100},
                       {"created_at": "2023-01-02", "value": 200}]
    # set testkey
    response = client.get("/data", headers={"X-API-KEY": "testkey"})
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert data["data"][0]["value"] == 100
    