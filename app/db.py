from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from settings import settings

engine = create_async_engine(url=settings.postgresql.get_conninfo())

new_session = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session