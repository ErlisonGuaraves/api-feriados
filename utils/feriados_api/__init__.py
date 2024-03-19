import aiohttp
import asyncio

class FeriadosAPI:
    def __init__(self, token, state='PB'):
        self.token = token
        self.state = state

    async def get_feriados(self, ano):
        async with aiohttp.ClientSession() as session:
            url = f'https://api.invertexto.com/v1/holidays/{ano}?token={self.token}&state={self.state}'
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Ocorreu o seguinte erro ao obter os feriados do ano {ano}: {response.status}")
