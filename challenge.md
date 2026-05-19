# API Quest – Backend Coding Challenge

## The 8 Levels

### Level 1: Ping
- `GET /ping` — Returns a simple acknowledgment (e.g., `{"message": "pong"}`)

### Level 2: Echo
- `POST /echo` — Accepts a JSON body and returns it back as-is

### Level 3: CRUD – Create & Read
- `POST /books` — Create a new book (title, author, etc.)
- `GET /books` — List all books
- `GET /books/:id` — Get a single book by ID

### Level 4: CRUD – Update & Delete
- `PUT /books/:id` — Update a book by ID
- `DELETE /books/:id` — Delete a book by ID

### Level 5: Auth Guard
- `POST /auth/token` — Authenticate and return a JWT token
- `GET /books` — Protected: requires valid JWT token

### Level 6: Search & Paginate
- `GET /books?author=X` — Filter books by author
- `GET /books?page=1&limit=2` — Paginate book results

### Level 7: Error Handling
- `POST /books` — Return proper validation errors for invalid input
- `GET /books/:id` — Return 404 for non-existent book

### Level 8: Boss – Speed Run
- All previous endpoints, optimized for performance

## Rules
- Use any language, framework, or tools. AI is encouraged.
- API must be publicly accessible.
- In-memory storage is fine — no database required.
- Levels must be completed in order.
- Unlimited retries allowed.
- Time budget: 2–4 hours.

## Tech Stack
- Python 3.11+
- FastAPI
- Uvicorn
- In-memory storage
- JWT for authentication
