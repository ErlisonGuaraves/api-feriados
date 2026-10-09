import aiohttp
import asyncio
from datetime import datetime, date

class FeriadosAPI:
    def __init__(self, token, state='SP'):
        self.token = token
        self.state = state

    async def get_feriados(self, ano):
        url = f'https://api.invertexto.com/v1/holidays/{ano}?token={self.token}&state={self.state}'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()

                # lê o body pra ajudar debug (sem explodir texto)
                body = await response.text()
                raise Exception(f"HTTP {response.status} - {body[:200]}")

    async def fetch_feriados(self, ano):
        print(f"Lendo feriados do ano: {ano}")

        tentativas = 5
        base_sleep = 2  # segundos

        for attempt in range(1, tentativas + 1):
            try:
                
                data_feriado_response = await self.get_feriados(ano)
                if not data_feriado_response:
                    return []

                rows = []
                for feriado in data_feriado_response:

                    dt = self._to_date(feriado['date'])
                    rows.append([
                        dt.strftime('%d/%m/%Y'),
                        self._dia_semana_pt(dt),
                        feriado['name']
                    ])
                return rows

            except Exception as e:
                msg = str(e)

                # retry só em erros temporários
                if any(code in msg for code in ["HTTP 429", "HTTP 500", "HTTP 502", "HTTP 503", "HTTP 504"]):
                    if attempt < tentativas:
                        sleep_s = base_sleep * attempt
                        print(f"[WARN] Ano {ano}: {msg} | retry {attempt}/{tentativas} em {sleep_s}s")
                        await asyncio.sleep(sleep_s)
                        continue

                # se não for temporário, ou acabou retry: não derruba o processo
                print(f"[ERRO] Ano {ano}: {msg}")
                return []

        return []


    def _to_date(self, value):
        if isinstance(value, date):
            return value
        return datetime.strptime(value, "%Y-%m-%d").date()

    def _dia_semana_pt(self, dt: date) -> str:
        dias = [
            "segunda-feira",
            "terça-feira",
            "quarta-feira",
            "quinta-feira",
            "sexta-feira",
            "sábado",
            "domingo",
        ]
        return dias[dt.weekday()]
