import csv

class CSVGenerator:
    def __init__(self, filename='feriados_total.csv'):
        self.filename = filename

    def generate_csv(self, data):
        with open(self.filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Ano', 'Data', 'Nome', 'Tipo'])
            writer.writerows(data)