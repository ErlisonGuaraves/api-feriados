import aiohttp
import asyncio
import csv
from utils.send_email import Send_email  # Importa a classe Send_email do seu arquivo send_email.py

async def getFeriados(ano):
    print("requisitando a api...")
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.invertexto.com/v1/holidays/{ano}?token=7033|ZVVQjtkDJ1c2ra1p34C0NMaigkQAUri7&state=PB') as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"ocorreu o seguinte erro: {response.status}") 

async def buscarDados(ano, response):
    print("buscando os dados...")
    feriados_formatados = []
    for data_feriado in response:
        date = data_feriado['date']
        name = data_feriado['name']
        type = data_feriado['type']
        feriados_formatados.append([ano, date, name, type])  
    return feriados_formatados

async def main():
    anos = list(range(2021, 2099+1))
    feriados_total = []

    for ano in anos:
        data_feriado_response = await getFeriados(ano)
        
        if data_feriado_response:
            feriados_formatados = await buscarDados(ano, data_feriado_response)
            feriados_total.extend(feriados_formatados)

    with open('feriados_total.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Ano', 'Data', 'Nome', 'Tipo'])
        writer.writerows(feriados_total)

    # Envia o email com o arquivo CSV como anexo
    #print("enviando o email..")
    #send_email = Send_email()
    #send_email.send_email()

if __name__ == '__main__':
    print("começando o processo de envio...")
    asyncio.run(main())
