import json
import requests

url = "https://b3de-104-28-250-40.eu.ngrok.io/pump"
headers = {'Content-type': 'application/json'}
data = open('control.json')
r = requests.post(url, data=data, headers=headers)