import sys
import requests
import json
import smtplib
import ssl
import ftplib
from fpdf import FPDF
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def sendMail(fromEmail: str, subject: str, text: str, toEmail: list):

    # Message 
    msg = MIMEMultipart()
    msg['From'] = fromEmail
    msg['To'] = ', '.join(toEmail)  
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    # Attach File to MIME
    fileToAttach = open('data.pdf', 'rb') 
    attachedfile = MIMEApplication(fileToAttach.read())
    attachedfile.add_header('content-disposition', 'attachment', filename = 'data.pdf' )
    msg.attach(attachedfile)

    # SMTP Login and Mail Service 
    port = 465
    password = ''
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL('smtp.gmail.com', port, context = context)
    server.login('', password)
    server.sendmail(fromEmail, toEmail, msg.as_string())
    server.close()

def getPlayerInformation(): 

    # Getting Player Informations
    playerTag = sys.argv[1]
    playerTag = playerTag.replace('#', '%23')
    playerToken = open('token.txt', 'r').read()
    playerEmail = sys.argv[2]

    # API Request
    baseURL = 'https://api.clashroyale.com/v1/players/' + playerTag
    headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + playerToken}
    call = requests.get(baseURL, headers = headers)
    response = call.json()

    # Write Request to Log File
    log = open('response.log', 'w')
    log.write(str(response))
    log.close()

    # Write Data to PDF
    pdf = FPDF(orientation = 'L', unit = 'mm', format='A4')
    pdf.add_page()
    pdf.image('bg.png', 0, 0, w = 300, h = 300)
    pdf.add_font('cr', '', 'cr.ttf', uni=True)
    pdf.set_font('cr', '', 16)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, 'Your Royale API Data!', 0, 0);
    pdf.ln(25)

    # Loop through API Call and fill the PDF
    responseKeys = ['tag', 'name', 'expLevel', 'trophies', 'bestTrophies', 'wins', 'losses']
    formatedKeys = ['Tag', 'Name', 'Current Level', 'Current Trophies', 'Highest Trophies', 'Total Wins', 'Total Losses']
    counter = 0
    for key in responseKeys: 
        # Workaround for PDF Cell
        value = str(response[key])
        latin = value.encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(200, 10, txt = formatedKeys[counter] + ': ' + latin, ln = 1)
        counter += 1
    pdf.output('data.pdf') 

    # Upload PDF to Server
    dt = datetime.date(datetime.now())
    session = ftplib.FTP()
    session.connect('', 21)
    session.login('', '')
    fileToUpload = open('data.pdf', 'rb')
    session.storbinary('STOR data-' + str(dt) + '.pdf', fileToUpload)
    fileToUpload.close()
    session.quit()

    # Mail Service
    sendMail(fromEmail = '', subject = 'Royale Api Data', text = 'Im Anhang finden Sie das PDF mit den Daten.', toEmail = playerEmail)

getPlayerInformation()