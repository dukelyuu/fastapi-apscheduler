from fastapi.testclient import TestClient
from src.webapp import app

client = TestClient(app)

def test_read_main():
    response = client.get("/api/task")
    assert response.status_code == 200
    assert response.json().get('health') != None