import asyncio
from utils.send_email import SendEmail  
from utils.generate_csv import CSVGenerator
from utils.feriados_api import FeriadosAPI


async def main():
    # Instanciação da classe FeriadosAPI
    api = FeriadosAPI(token='7033|ZVVQjtkDJ1c2ra1p34C0NMaigkQAUri7', state='PB')

    # Anos para os quais você deseja obter os feriados
    anos = list(range(2021, 2022))

    feriados_total = []

    for ano in anos:
        # Chamada ao método get_feriados da classe FeriadosAPI
        data_feriado_response = await api.get_feriados(ano)
        
        if data_feriado_response:
            feriados_formatados = [[ano, feriado['date'], feriado['name'], feriado['type']] for feriado in data_feriado_response]
            feriados_total.extend(feriados_formatados)

    
    #gera o csv
    csv_generator = CSVGenerator()
    csv_generator.generate_csv(feriados_formatados)

    #Envia o email com o arquivo CSV como anexo  
    print("enviando o email..")
    send_email = SendEmail("erlison.santos@guaraves.com.br","kaua.vinicius@guaraves.com.br" )
    send_email.send_email()

   

if __name__ == '__main__':
    print("começando o processo de envio...")
    asyncio.run(main())

