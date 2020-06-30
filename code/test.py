import requests
import json

def call():
    response = requests.post(url = 'http://0.0.0.0:5000/jan/ls')
    return json.loads(response.text)

def ping():
    response = requests.post(url = 'http://0.0.0.0:5000/ping')
    return response.text

if __name__ == '__main__':
    print(ping())
    print(call())