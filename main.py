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
    fileToAttach = open('data.pdf', "rb") 
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
    print('Getting Data...')

    # Write Request to Log File
    log = open('response.log', 'w')
    log.write(str(response))
    log.close()

    # Write Data to PDF
    pdf = FPDF(orientation = 'P', unit = 'mm', format='A4')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Your Royale API Data!', 0, 1)
    pdf.ln(25)

    # Loop through API Call and fill the PDF
    responseKeys = ['tag', 'name', 'expLevel', 'trophies', 'bestTrophies', 'wins', 'losses']
    formatedKeys = ['Player Tag', 'Player Name', 'Player Level', 'Player Trophies', 'Player Best Trophies', 'Player Wins', 'Player Losses']
    counter = 0
    for key in responseKeys: 
        # Workaround for PDF Cell
        value = str(response[key])
        latin = value.encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(200, 10, txt = formatedKeys[counter] + ': ' + latin, ln = 1, align = 'C')
        counter += 1

    pdf.output('data.pdf') 
    print('PDF created...')

    # Upload PDF to Server
    dt = datetime.date(datetime.now())
    session = ftplib.FTP()
    session.connect('', 21)
    session.login('','')
    fileToUpload = open('data.pdf', 'rb')
    session.storbinary('STOR data-' + str(dt) + '.pdf', fileToUpload)
    fileToUpload.close()
    session.quit()
    print('PDF uploaded...')

    # Mail Service
    sendMail(fromEmail = '', subject = 'Royale Api Data', text = 'Vielen Dank, im Anhang finden Sie das PDF mit den Daten.', toEmail = playerEmail)
    print('Email sent...')

getPlayerInformation()