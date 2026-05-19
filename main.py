import json
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from jose import jwt
from pydantic import BaseModel

app = FastAPI()


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


def create_access_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


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
