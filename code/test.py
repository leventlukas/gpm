import requests
import json

def call():
    response = requests.post(url = 'http://0.0.0.0:5000/jan/ls')
    return json.loads(response.text)

if __name__ == '__main__':
    print(call())