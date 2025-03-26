from typing import Annotated, List
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db import get_session
from schema import TRXAdressAddSchema, TRXAdressSchema
from models import create_db, TRXAdressModel


session_dep = Annotated[AsyncSession, Depends(get_session)]

app = FastAPI()


@app.post(
    "/get_adress_info",
    summary="Получить информацию по адресу TRX кошелька",
    description="Эндпоинт возвращает bandwidth, energy, и баланс trx",
)
async def get_adress_info(data: TRXAdressAddSchema, session: session_dep):
    new_trx_adress = TRXAdressModel(trx_adress=data.trx_adress)
    session.add(new_trx_adress)
    await session.commit()
    return {"adress": data.trx_adress}

@app.get(
    "/get_reqests",
    summary="Получить список запросов к сервису",
    description="Эндпоинт возвращает список кошельков, по которым запрашивалась информация",
)
async def get_requests(session: session_dep) -> List[TRXAdressSchema]:
    query = select(TRXAdressModel)
    result = await session.execute(query)
    return result.scalars().all()

@app.post("/db")
async def db() -> None:
    await create_db()
