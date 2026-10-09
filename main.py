import asyncio
from os import getenv
 
from utils.generate_csv import CSVGenerator
from utils.feriados_api import FeriadosAPI
from dotenv import load_dotenv

async def main():
    load_dotenv() 
    api = FeriadosAPI(token=f'{getenv("token")}', state='SP')
    anos = list(range(2021, 2099 + 1))
    print(getenv("token"))
    # multiplas requisições executadas ao mesmo tempo, de forma paralela 🤓
    results = await asyncio.gather(*(api.fetch_feriados(ano) for ano in anos))

    # Filtra e combina os resultados
    feriados_total = [feriado for result in results for feriado in result]

    # Gera o CSV
    csv_generator = CSVGenerator()
    csv_generator.generate_csv(feriados_total)

    print("Processo concluído")
   

if __name__ == '__main__':
    print("começando o processo...")
    asyncio.run(main())

