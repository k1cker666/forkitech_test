from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from db import engine


class Base(DeclarativeBase):
    pass


class TRXAdressModel(Base):
    __tablename__ = "trx_adress"

    id: Mapped[int] = mapped_column(primary_key=True)
    trx_adress: Mapped[str] = mapped_column()


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)