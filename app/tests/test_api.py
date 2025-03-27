from datetime import datetime
from unittest.mock import AsyncMock
import pytest
from httpx import ASGITransport, AsyncClient

from models import TRXAddressModel
from repository import TRXRepository
from main import app, get_repository


@pytest.mark.asyncio
async def test_get_requests_empty():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/get_requests")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_requests_non_empty_mocked():
    mock_repo = AsyncMock(spec=TRXRepository)
    mock_data = TRXAddressModel(id=1, trx_address="TKESvnc7KfKRP7me56twasvAtxLK3ptXEv", added_at=datetime.now())
    mock_repo.get_all_addresses.return_value = [mock_data]
    
    app.dependency_overrides[get_repository] = lambda: mock_repo
    
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:
        response = await ac.get("/get_requests")
    
    assert response.status_code == 200
    json = response.json()[0]
    assert json.get("trx_address") == mock_data.trx_address
    assert json.get("added_at") == mock_data.added_at.strftime("%Y-%m-%d %H:%M:%S")

    app.dependency_overrides.clear()