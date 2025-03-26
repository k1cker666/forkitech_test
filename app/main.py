from fastapi import FastAPI
from schema import TRXAdressSchema
from models import create_db


app = FastAPI()

@app.get("/", summary="Пинг ручка")
def ping():
    return {"ping": "pong"}

@app.post("/db")
async def db() -> None:
    await create_db()
