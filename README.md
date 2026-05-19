# API Quest – Backend Coding Challenge

FastAPI REST API with JWT auth, CRUD books, search/pagination, and SQLite storage.

## Tech Stack

- Python 3.11+
- FastAPI + Uvicorn
- SQLite (stdlib `sqlite3`)
- JWT via `python-jose`
- Pytest + httpx

## Setup

```bash
git clone <repo-url>
cd backendchallenge
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Env Vars

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_PATH` | `books.db` | SQLite database path |
| `API_PREFIX` | `http://localhost:8000` | API base URL for tests |

## Manual Testing with curl

```bash
API_PREFIX="${API_PREFIX:-http://localhost:8000}"

# 1. Ping
curl "$API_PREFIX/ping"

# 2. Echo
curl -X POST "$API_PREFIX/echo" \
  -H "Content-Type: application/json" \
  -d '{"hello":"world"}'

# 3. Empty echo
curl -X POST "$API_PREFIX/echo"

# 4. Get token
curl -X POST "$API_PREFIX/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password123"}'

# 5. Save token
TOKEN=$(curl -s -X POST "$API_PREFIX/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password123"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# 6. Create book
curl -X POST "$API_PREFIX/books" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"1984","author":"Orwell"}'

curl -X POST "$API_PREFIX/books" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"Animal Farm","author":"Orwell"}'

curl -X POST "$API_PREFIX/books" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"The Old Man and the Sea","author":"Hemingway"}'

# 7. List all books
curl "$API_PREFIX/books" \
  -H "Authorization: Bearer $TOKEN"

# 8. Get book by ID (replace with actual ID from list)
BOOK_ID="<book-id>"
curl "$API_PREFIX/books/$BOOK_ID" \
  -H "Authorization: Bearer $TOKEN"

# 9. Update book
curl -X PUT "$API_PREFIX/books/$BOOK_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"Animal Farm (Updated)","author":"George Orwell"}'

# 10. Delete book
curl -X DELETE "$API_PREFIX/books/$BOOK_ID" \
  -H "Authorization: Bearer $TOKEN"

# 11. Search by author
curl "$API_PREFIX/books?author=Orwell" \
  -H "Authorization: Bearer $TOKEN"

# 12. Search by title
curl "$API_PREFIX/books?title=1984" \
  -H "Authorization: Bearer $TOKEN"

# 13. Search by title + author
curl "$API_PREFIX/books?title=1984&author=Orwell" \
  -H "Authorization: Bearer $TOKEN"

# 14. Paginate
curl "$API_PREFIX/books?page=1&limit=2" \
  -H "Authorization: Bearer $TOKEN"

# 15. Filter + paginate
curl "$API_PREFIX/books?author=Orwell&page=1&limit=1" \
  -H "Authorization: Bearer $TOKEN"

# 16. No auth (should fail)
curl "$API_PREFIX/books"

# 17. Invalid token
curl "$API_PREFIX/books" \
  -H "Authorization: Bearer invalid"

# 18. Validation error – missing title
curl -X POST "$API_PREFIX/books" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"author":"NoTitle"}'

# 19. Validation error – auth endpoint (shows contact message)
curl -X POST "$API_PREFIX/auth/token"
```

## Automated Tests

```bash
# Run all tests
python -m pytest test_main.py -v

# Run a specific test
python -m pytest test_main.py::test_ping -v

# Run tests matching a pattern
python -m pytest test_main.py -v -k "books"
```

### Test Architecture

`conftest.py` provides fixtures:
- `client` — `TestClient` with temp SQLite database per session
- `auth_token` — JWT from admin login
- `auth_headers` — `Authorization` header dict

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/ping` | No | Health check |
| `POST` | `/echo` | No | Echo JSON body |
| `POST` | `/auth/token` | No | Get JWT token |
| `POST` | `/books` | JWT | Create a book |
| `GET` | `/books` | JWT | List / search / paginate books |
| `GET` | `/books/{id}` | JWT | Get book by ID |
| `PUT` | `/books/{id}` | JWT | Update book by ID |
| `DELETE` | `/books/{id}` | JWT | Delete book by ID |

### GET /books query params

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `title` | `string` | — | Filter by title (LIKE match) |
| `author` | `string` | — | Filter by author (LIKE match) |
| `page` | `int` | `1` | Page number |
| `limit` | `int` | `10` | Items per page (max 100) |

Response:

```json
{
  "data": [{ "id": "...", "title": "1984", "author": "Orwell" }],
  "total": 1,
  "page": 1,
  "limit": 10
}
```

## Default Credentials

| Username | Password |
|----------|----------|
| `admin` | `password123` |
