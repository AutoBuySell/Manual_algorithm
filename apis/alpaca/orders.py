import requests
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

baseurl = os.getenv('ALPACA_PAPER_BASEURL')

headers = {
  'accept': 'application/json',
  'content-type': 'application/json',
  'APCA-API-KEY-ID': os.getenv('ALPACA_PAPER_KEY'),
  'APCA-API-SECRET-KEY': os.getenv('ALPACA_PAPER_KEY_SECRET'),
}

def buy_order(asset, buy_power):
  payload = {
    'side': 'buy',
    'type': 'market',
    'time_in_force': 'day',
    'symbol': asset,
    'notional': buy_power,
  }

  response = requests.post(baseurl + '/orders', json=payload, headers=headers).json()

  return response

def sell_order(asset, qty):
  payload = {
    'side': 'sell',
    'type': 'market',
    'time_in_force': 'day',
    'symbol': asset,
    'qty': qty,
  }

  response = requests.post(baseurl + '/orders', json=payload, headers=headers).json()

  return response

