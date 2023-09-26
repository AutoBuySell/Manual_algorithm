import requests
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

dataServerUrl = os.getenv('DATA_SERVER_URL')

headers = {
    'accept': 'application/json',
}

def req_data_realtime(symbols):
    response = requests.post(
        url=dataServerUrl + '/dataArchiving/real_time',
        headers=headers,
        json={
            'symbols': symbols,
        }
    )

    if response.status_code == 201:
        print(response.json())