import json
import os
import sqlite3
import uuid
from contextlib import asynccontextmanager, contextmanager
from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from pydantic import BaseModel


def get_db_path() -> str:
    return os.environ.get("DB_PATH", "books.db")


def init_db():
    conn = sqlite3.connect(get_db_path())
    conn.execute(
        "CREATE TABLE IF NOT EXISTS books (id TEXT PRIMARY KEY, title TEXT NOT NULL, author TEXT NOT NULL)"
    )
    conn.commit()
    conn.close()


@contextmanager
def get_db():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid request. Please contact ngurahbaskara@gmail.com for assistance."},
    )


SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

USERS = {"admin": "password123"}


class AuthRequest(BaseModel):
    username: str
    password: str


class BookCreate(BaseModel):
    title: str
    author: str


class BookResponse(BaseModel):
    id: str
    title: str
    author: str


def create_access_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials. Please contact ngurahbaskara@gmail.com for assistance.",
        )
    token = authorization[len("Bearer "):]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials. Please contact ngurahbaskara@gmail.com for assistance.",
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials. Please contact ngurahbaskara@gmail.com for assistance.",
        )


@app.get("/ping")
def ping():
    return {"message": "pong"}


@app.post("/echo")
async def echo(request: Request):
    body = await request.body()
    if not body:
        return None
    return json.loads(body)


@app.post("/auth/token")
def auth_token(data: AuthRequest):
    password = USERS.get(data.username)
    if password is None or password != data.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials. Please contact ngurahbaskara@gmail.com for assistance.",
        )
    token = create_access_token(data.username)
    return {"access_token": token, "token_type": "bearer"}


@app.post("/books", status_code=201, response_model=BookResponse)
def create_book(book: BookCreate, _=Depends(get_current_user)):
    book_id = str(uuid.uuid4())
    with get_db() as conn:
        conn.execute(
            "INSERT INTO books (id, title, author) VALUES (?, ?, ?)",
            (book_id, book.title, book.author),
        )
        conn.commit()
    return {"id": book_id, "title": book.title, "author": book.author}


@app.get("/books", response_model=list[BookResponse])
def list_books(_=Depends(get_current_user)):
    with get_db() as conn:
        rows = conn.execute("SELECT id, title, author FROM books").fetchall()
    return [dict(row) for row in rows]


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: str, _=Depends(get_current_user)):
    with get_db() as conn:
        row = conn.execute(
            "SELECT id, title, author FROM books WHERE id = ?", (book_id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return dict(row)


@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: str, book: BookCreate, _=Depends(get_current_user)):
    with get_db() as conn:
        row = conn.execute(
            "SELECT id FROM books WHERE id = ?", (book_id,)
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Book not found")
        conn.execute(
            "UPDATE books SET title = ?, author = ? WHERE id = ?",
            (book.title, book.author, book_id),
        )
        conn.commit()
    return {"id": book_id, "title": book.title, "author": book.author}


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: str, _=Depends(get_current_user)):
    with get_db() as conn:
        row = conn.execute(
            "SELECT id FROM books WHERE id = ?", (book_id,)
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Book not found")
        conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
