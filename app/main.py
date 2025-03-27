from typing import List
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy import AsyncTron
from tronpy.exceptions import BadAddress

from repository import TRXRepository
from deps import get_session, get_client
from schema import TRXAddressAddSchema, TRXAddressSchema, TRXAdressInfoSchema
from service import TronClient


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
    try:
        await repo.add_address(data.trx_address)
        account_info = await client.get_account_info(data.trx_address)
    except BadAddress as e:
        await repo.rollback()
        raise HTTPException(status_code=400, detail="Bad trx address")
    except Exception:
        await repo.rollback()
        raise HTTPException(status_code=500, detail="Something went wrong")
    await repo.commit()
    return account_info

@app.get(
    "/get_requests",
    summary="Получить список запросов к сервису",
    description="Эндпоинт возвращает список кошельков, по которым запрашивалась информация",
)
async def get_requests(
    repo: TRXRepository = Depends(get_repository),
    size: int = Query(5, ge=1, le=100),
    page: int = Query(1, ge=1)
) -> List[TRXAddressSchema]:
    result = await repo.get_all_addresses(size=size, page=page)
    return [TRXAddressSchema.model_validate(addr) for addr in result]
