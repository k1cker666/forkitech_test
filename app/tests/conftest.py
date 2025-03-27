import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from models import Base

DB_URL = "postgresql+asyncpg://postgres:postgres@localhost:5002/test_db"

engine = create_async_engine(DB_URL, echo=False)
test_session = async_sessionmaker(engine, expire_on_commit=False)

@pytest_asyncio.fixture
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def session():
    async with test_session() as session:
        yield session

