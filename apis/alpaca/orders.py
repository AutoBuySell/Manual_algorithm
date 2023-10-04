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

def buy_order(symbol, qty):
  payload = {
    'side': 'buy',
    'type': 'market',
    'time_in_force': 'day',
    'symbol': symbol,
    'qty': qty,
  }

  response = requests.post(
    baseurl + '/orders',
    json=payload,
    headers=headers
  ).json()

  orderInfo = {
    'orderId': response['id'],
  }

  return orderInfo

def sell_order(symbol, qty):
  payload = {
    'side': 'sell',
    'type': 'market',
    'time_in_force': 'day',
    'symbol': symbol,
    'qty': qty,
  }

  response = requests.post(
    baseurl + '/orders',
    json=payload,
    headers=headers
  ).json()

  orderInfo = {
    'orderId': response['id'],
  }

  return orderInfo

def get_order(orderId: str):
  response = requests.get(
    baseurl + '/orders' + f'/{orderId}',
    headers=headers
  ).json()

  new_info = {
    'status': response['status'],
    'filledQty': response['filled_qty'],
    'filledAvgPrice': response['filled_avg_price'],
  }

  return new_info
