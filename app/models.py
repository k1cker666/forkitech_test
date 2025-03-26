from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from db import engine


class Base(DeclarativeBase):
    pass


class TRXAddressModel(Base):
    __tablename__ = "trx_address"

    id: Mapped[int] = mapped_column(primary_key=True)
    trx_address: Mapped[str] = mapped_column(String(34))
    added_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.now())


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)