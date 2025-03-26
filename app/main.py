from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from repository import TRXRepository
from db import get_session
from schema import TRXAdressAddSchema, TRXAdressSchema
from models import create_db


app = FastAPI()

async def get_repository(session: AsyncSession = Depends(get_session)):
    return TRXRepository(session)

@app.post(
    "/get_adress_info",
    summary="Получить информацию по адресу TRX кошелька",
    description="Эндпоинт возвращает bandwidth, energy, и баланс trx",
)
async def get_adress_info(data: TRXAdressAddSchema, repo: TRXRepository = Depends(get_repository)):
    await repo.add_address(data.trx_adress)
    return {"adress": data.trx_adress}

@app.get(
    "/get_reqests",
    summary="Получить список запросов к сервису",
    description="Эндпоинт возвращает список кошельков, по которым запрашивалась информация",
)
async def get_requests(repo: TRXRepository = Depends(get_repository)) -> List[TRXAdressSchema]:
    result = await repo.get_all_addresses()
    return [TRXAdressSchema.model_validate(addr) for addr in result]


@app.post("/db")
async def db() -> None:
    await create_db()
