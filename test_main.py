from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}


def test_echo_valid_json():
    payload = {"hello": "world", "num": 42}
    response = client.post("/echo", json=payload)
    assert response.status_code == 200
    assert response.json() == payload


def test_echo_nested():
    payload = {"data": {"nested": [1, 2, 3], "deep": {"key": "value"}}}
    response = client.post("/echo", json=payload)
    assert response.status_code == 200
    assert response.json() == payload


def test_echo_array():
    payload = [1, 2, 3, "four"]
    response = client.post("/echo", json=payload)
    assert response.status_code == 200
    assert response.json() == payload
