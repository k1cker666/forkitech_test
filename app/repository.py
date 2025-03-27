from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import TRXAddressModel


class TRXRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_address(self, trx_address: str) -> TRXAddressModel:
        new_address = TRXAddressModel(trx_address=trx_address)
        self.session.add(new_address)
        return new_address

    async def get_all_addresses(self, size, page) -> Sequence[TRXAddressModel]:
        offset = size*(page-1)
        query = select(TRXAddressModel).limit(size).offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()