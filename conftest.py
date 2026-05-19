import os
import tempfile

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)
    old_db_path = os.environ.get("DB_PATH")
    os.environ["DB_PATH"] = db_path

    from main import app

    with TestClient(app) as c:
        yield c

    if old_db_path:
        os.environ["DB_PATH"] = old_db_path
    else:
        del os.environ["DB_PATH"]
    os.unlink(db_path)


@pytest.fixture
def auth_token(client):
    response = client.post(
        "/auth/token",
        json={"username": "admin", "password": "password123"},
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}
