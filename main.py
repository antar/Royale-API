import requests
import json

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
    response = (json.dumps(call.json(), indent = 2))

    # Write Request to Log File
    log = open('log.txt', 'w')
    log.write(response)
    log.close()

    print(response)

getPlayerInformation()

