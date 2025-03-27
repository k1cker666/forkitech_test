import pytest

from repository import TRXRepository
from models import TRXAddressModel

@pytest.mark.asyncio
async def test_add_address_success(session, setup_db):
    repo = TRXRepository(session)
    test_address = "TKESvnc7KfKRP7me56twasvAtxLK3ptXEv"

    result = await repo.add_address(test_address)
    await repo.commit()

    assert result.id is not None
    assert result.trx_address == test_address

    check_result = await session.get(TRXAddressModel, result.id)

    assert check_result is not None
    assert check_result.trx_address == test_address