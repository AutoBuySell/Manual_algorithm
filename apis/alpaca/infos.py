import requests
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

baseurl = os.getenv('ALPACA_PAPER_BASEURL')

headers = {
  'accept': 'application/json',
  'APCA-API-KEY-ID': os.getenv('ALPACA_PAPER_KEY'),
  'APCA-API-SECRET-KEY': os.getenv('ALPACA_PAPER_KEY_SECRET'),
}

def get_buy_power():
  response = requests.get(baseurl + '/account', headers=headers).json()

  return response['buying_power']

def get_current_positions():
  response = requests.get(baseurl + '/positions', headers=headers).json()

  return {r['symbol']: r['qty'] for r in response if r['side'] == 'long'}
