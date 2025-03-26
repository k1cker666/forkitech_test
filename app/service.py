from tronpy import AsyncTron

from schema import TRXAdressInfoSchema


class TronClient:
    def __init__(self, client: AsyncTron):
        self.client = client

    async def get_account_info(self, trx_address: str):
        trx_balance = await self.client.get_account_balance(trx_address)
        bandwidth = await self.client.get_bandwidth(trx_address)
        energy = await self._get_account_energy(trx_address)
        data = TRXAdressInfoSchema(
            trx_address=trx_address,
            trx_balance=trx_balance,
            bandwidth=bandwidth,
            energy=energy,
        )
        return data

    async def _get_account_energy(self, trx_address: str) -> int:
        account_resources = await self.client.get_account_resource(trx_address)
        energy_limit = account_resources.get("EnergyLimit", 0)
        energy_used = account_resources.get("EnergyUsed", 0)
        return energy_limit - energy_used