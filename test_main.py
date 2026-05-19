def test_ping(client):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}


def test_echo_valid_json(client):
    payload = {"hello": "world", "num": 42}
    response = client.post("/echo", json=payload)
    assert response.status_code == 200
    assert response.json() == payload


def test_echo_nested(client):
    payload = {"data": {"nested": [1, 2, 3], "deep": {"key": "value"}}}
    response = client.post("/echo", json=payload)
    assert response.status_code == 200
    assert response.json() == payload


def test_echo_array(client):
    payload = [1, 2, 3, "four"]
    response = client.post("/echo", json=payload)
    assert response.status_code == 200
    assert response.json() == payload


def test_echo_empty(client):
    response = client.post("/echo")
    assert response.status_code == 200
    assert response.json() is None


def test_auth_token_valid(client):
    response = client.post(
        "/auth/token",
        json={"username": "admin", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_auth_token_invalid_password(client):
    response = client.post(
        "/auth/token",
        json={"username": "admin", "password": "wrong"},
    )
    assert response.status_code == 401
    assert "ngurahbaskara@gmail.com" in response.json()["detail"]


def test_auth_token_unknown_user(client):
    response = client.post(
        "/auth/token",
        json={"username": "nobody", "password": "x"},
    )
    assert response.status_code == 401
    assert "ngurahbaskara@gmail.com" in response.json()["detail"]


def test_create_book(client, auth_headers):
    response = client.post(
        "/books",
        json={"title": "1984", "author": "George Orwell"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "1984"
    assert data["author"] == "George Orwell"
    assert "id" in data


def test_list_books(client, auth_headers):
    client.post("/books", json={"title": "A", "author": "X"}, headers=auth_headers)
    client.post("/books", json={"title": "B", "author": "Y"}, headers=auth_headers)
    response = client.get("/books", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_book(client, auth_headers):
    created = client.post(
        "/books", json={"title": "Dune", "author": "Herbert"}, headers=auth_headers
    )
    book_id = created.json()["id"]
    response = client.get(f"/books/{book_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Dune"


def test_get_book_404(client, auth_headers):
    response = client.get("/books/nonexistent-id", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_update_book(client, auth_headers):
    created = client.post(
        "/books", json={"title": "Old", "author": "Old"}, headers=auth_headers
    )
    book_id = created.json()["id"]
    response = client.put(
        f"/books/{book_id}",
        json={"title": "New", "author": "New"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["title"] == "New"
    assert response.json()["author"] == "New"


def test_update_book_404(client, auth_headers):
    response = client.put(
        "/books/nonexistent-id",
        json={"title": "X", "author": "Y"},
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_delete_book(client, auth_headers):
    created = client.post(
        "/books", json={"title": "Del", "author": "Me"}, headers=auth_headers
    )
    book_id = created.json()["id"]
    response = client.delete(f"/books/{book_id}", headers=auth_headers)
    assert response.status_code == 204
    response = client.get(f"/books/{book_id}", headers=auth_headers)
    assert response.status_code == 404


def test_delete_book_404(client, auth_headers):
    response = client.delete("/books/nonexistent-id", headers=auth_headers)
    assert response.status_code == 404


def test_books_no_token(client):
    response = client.get("/books")
    assert response.status_code == 422
    assert "ngurahbaskara@gmail.com" in response.json()["detail"]


def test_books_invalid_token(client):
    response = client.get("/books", headers={"Authorization": "Bearer invalid"})
    assert response.status_code == 401
    assert "ngurahbaskara@gmail.com" in response.json()["detail"]


def test_books_wrong_token_prefix(client):
    response = client.get("/books", headers={"Authorization": "Token xxx"})
    assert response.status_code == 401
    assert "ngurahbaskara@gmail.com" in response.json()["detail"]
