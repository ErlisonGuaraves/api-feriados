import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os

class Send_email:
    def __init__(self):
        load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env
        self.from_email = os.getenv('EMAIL_FROM')
        self.to_email = os.getenv('EMAIL_TO')
        self.password = os.getenv('PASS_KEY')

    def send_email(self):
        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['To'] = self.to_email
        msg['Subject'] = "Teste de Envio de Email"

        # Lendo o conteúdo do arquivo CSV
        with open('feriados_total.csv', 'rb') as file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename=feriados_total.csv")
            msg.attach(part)

        text = msg.as_string()
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(self.from_email, self.password)
            server.sendmail(self.from_email, self.to_email, text)


