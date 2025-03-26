from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy import AsyncTron

from repository import TRXRepository
from deps import get_session, get_client
from schema import TRXAddressAddSchema, TRXAddressSchema, TRXAdressInfoSchema
from service import TronClient
from models import create_db


app = FastAPI()

async def get_repository(session: AsyncSession = Depends(get_session)):
    return TRXRepository(session)

async def get_tron_client(client: AsyncTron = Depends(get_client)):
    return TronClient(client)

@app.post(
    "/get_address_info",
    summary="Получить информацию по адресу TRX кошелька",
    description="Эндпоинт возвращает bandwidth, energy, и баланс trx",
)
async def get_address_info(
    data: TRXAddressAddSchema,
    repo: TRXRepository = Depends(get_repository),
    client: TronClient = Depends(get_tron_client)
) -> TRXAdressInfoSchema:
    await repo.add_address(data.trx_address)
    account_info = await client.get_account_info(data.trx_address)
    return account_info

@app.get(
    "/get_requests",
    summary="Получить список запросов к сервису",
    description="Эндпоинт возвращает список кошельков, по которым запрашивалась информация",
)
async def get_requests(repo: TRXRepository = Depends(get_repository)) -> List[TRXAddressSchema]:
    result = await repo.get_all_addresses()
    return [TRXAddressSchema.model_validate(addr) for addr in result]
