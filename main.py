import json

from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/ping")
def ping():
    return {"message": "pong"}


@app.post("/echo")
async def echo(request: Request):
    body = await request.body()
    if not body:
        return None
    return json.loads(body)
