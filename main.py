import requests
import json
from fpdf import FPDF


def getPlayerInformation(): 

    # Getting Players Tag
    playerTag = input('Please enter your player tag: ')
    playerTag = playerTag.replace('#', '%23')

    # Read Token FIle
    playerToken = open('token.txt', 'r').read()

    # API URL
    baseURL = 'https://api.clashroyale.com/v1/players/' + playerTag

    # API Request
    headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + playerToken}
    call = requests.get(baseURL, headers=headers)
    response = call.json()

    # Write Request to Log File
    log = open('response.log', 'w')
    log.write(str(response))
    log.close()

    # Write Data to PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size = 15)

    # Loop through API Call and fill the PDF
    responseKeys = ['tag', 'name', 'expLevel', 'trophies', 'bestTrophies', 'wins', 'losses']

    for key in responseKeys: 
        # Workaround for PDF Cell
        value = str(response[key])
        latin = value.encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(200, 10, txt = key + ': ' + latin, ln = 1, align = 'C')

    pdf.output('data.pdf') 

    print('PDF created...')

getPlayerInformation()