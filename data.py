import sys
import requests
import json
import smtplib
import ssl
import ftplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from fpdf import FPDF, HTMLMixin

class MyFPDF(FPDF, HTMLMixin):
    pass

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
    password = 'EmailPassword'
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL('smtp.gmail.com', port, context = context)
    server.login('Email', password)
    server.sendmail(fromEmail, toEmail, msg.as_string())
    server.close()

def getPlayerInformation(): 

    # Getting Player Informations
    playerTag = sys.argv[1]
    playerTag = playerTag.replace('#', '%23')
    playerToken = open('token.txt', 'r').read()
    if len(sys.argv) == 3:
        playerEmail = sys.argv[2]

    # Get Last Season for API Call
    today = datetime.date.today()
    first = today.replace(day = 1)
    lastMonth = first - datetime.timedelta(days = 1)
    lastSeason = lastMonth.strftime('%Y-%m')

    # API Requests
    baseURL = 'https://api.clashroyale.com/v1/'
    playerInformations = baseURL + 'players/' + playerTag
    topPlayersInformations = baseURL + 'locations/global/seasons/' + lastSeason + '/rankings/players'
    headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + playerToken}
    callPlayerInformations = requests.get(playerInformations, headers = headers)
    responsePlayerInformations = callPlayerInformations.json()
    callTopPlayerInformations = requests.get(topPlayersInformations, headers = headers)
    responseTopPlayerInformations = callTopPlayerInformations.json()

    # Write Requests to Log File
    firstLog = open('responsePlayerInformations.log', 'w')
    firstLog.write(str(responsePlayerInformations))
    firstLog.close()

    secondLog = open('responseTopPlayerInformations.log', 'w')
    secondLog.write(str(responseTopPlayerInformations))
    secondLog.close()

    # Write Data to PDF
    pdf = MyFPDF(orientation = 'L', unit = 'mm', format='A4')
    pdf.add_page()
    pdf.image('bg.png', 0, 0, w = 300, h = 300)
    pdf.add_font('cr', '', 'cr.ttf', uni = True)
    pdf.set_font('cr', '', 25)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, 'Your Royale API Data!', 0, 0);
    pdf.ln(30)
    pdf.set_font('cr', '', 20)
    pdf.set_text_color(0, 255, 223)
    pdf.cell(0, 0, 'Player Informations:', 0, 1);
    pdf.ln(10)

    # Loop through API Call and fill the PDF for Player Informations
    responseKeysPlayerInformations = ['tag', 'name', 'expLevel', 'trophies', 'bestTrophies', 'wins', 'losses']
    formatedKeysPlayerInformations = ['Tag', 'Name', 'Current Level', 'Current Trophies', 'Highest Trophies', 'Total Wins', 'Total Losses']
    counter = 0
    for key in responseKeysPlayerInformations: 
        # Workaround for PDF Cell
        value = str(responsePlayerInformations[key])
        latin = value.encode('latin-1', 'replace').decode('latin-1')
        pdf.set_font('cr', '', 15)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(200, 10, txt = formatedKeysPlayerInformations[counter] + ': ' + latin, ln = 1)
        counter += 1
    pdf.ln(20)
    pdf.set_font('cr', '', 20)
    pdf.set_text_color(0, 255, 223)
    pdf.cell(0, 0, 'Last Season Top Player:', 0, 1);
    pdf.ln(10)

    # Loop through API Call and fill the PDF for Top Player Informations
    responseKeysTopPlayersInformations = ['tag', 'name', 'trophies']
    formatedKeysTopPlayersInformations = ['Tag', 'Name', 'Season Trophies']
    counter = 0
    for key in responseKeysTopPlayersInformations:
        # Workaround for PDF Cell
        value = str(responseTopPlayerInformations['items'][0][key])
        latin = value.encode('latin-1', 'replace').decode('latin-1')
        pdf.set_font('cr', '', 15)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(200, 10, txt = formatedKeysTopPlayersInformations[counter] + ': ' + latin, ln = 1)
        counter += 1
    pdf.output('data.pdf') 

    # Upload PDF to Server
    # session = ftplib.FTP()
    # session.connect('ServerName', 21)
    # session.login('ServerUsername', 'ServerPassword')
    # fileToUpload = open('data.pdf', 'rb')
    # session.storbinary('STOR data' + '.pdf', fileToUpload)
    # fileToUpload.close()
    # session.quit()

    # Mail Service
    # sendMail(fromEmail = 'fromEmail', subject = 'Royale Api Data', text = 'Im Anhang finden Sie das PDF mit den Daten.', toEmail = playerEmail)

getPlayerInformation()