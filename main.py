import asyncio
from os import getenv
 
from utils.generate_csv import CSVGenerator
from utils.feriados_api import FeriadosAPI


async def main():
    # Instanciação da classe FeriadosAPI
    api = FeriadosAPI(token=f'{getenv("token")}', state='PB')

    # Anos para os quais você deseja obter os feriados
    anos = list(range(2021, 2099+1))

    feriados_total = []

    for ano in anos:
        data_feriado_response = await api.get_feriados(ano)
        print(f'processando feriados de: {ano}')
        if data_feriado_response:
            feriados_formatados = [[ano, feriado['date'], feriado['name'], feriado['type']] for feriado in data_feriado_response]
            feriados_total.extend(feriados_formatados)

    
    #gera o csv
    csv_generator = CSVGenerator()
    csv_generator.generate_csv(feriados_total)

    print("processo concluido")
   

if __name__ == '__main__':
    print("começando o processo...")
    asyncio.run(main())

