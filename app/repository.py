from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import TRXAdressModel

class TRXRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_address(self, trx_address: str) -> TRXAdressModel:
        new_address = TRXAdressModel(trx_adress=trx_address)
        self.session.add(new_address)
        await self.session.commit()
        return new_address

    async def get_all_addresses(self) -> Sequence[TRXAdressModel]:
        query = select(TRXAdressModel)
        result = await self.session.execute(query)
        return result.scalars().all()
