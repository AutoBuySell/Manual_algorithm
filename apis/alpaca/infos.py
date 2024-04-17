import requests
import os
import traceback
from dotenv import load_dotenv

from apps.error import CustomError

load_dotenv(verbose=True)

baseurl = os.getenv('ALPACA_PAPER_BASEURL')

headers = {
  'accept': 'application/json',
  'APCA-API-KEY-ID': os.getenv('ALPACA_PAPER_KEY'),
  'APCA-API-SECRET-KEY': os.getenv('ALPACA_PAPER_KEY_SECRET'),
}

def get_infos():
  '''
  return current account information including buying_power
  '''

  try:
    response = requests.get(baseurl + '/account', headers=headers)

    assert response.status_code == 200, response.json()

    response = response.json()

    return response

  except:
    print(traceback.format_exc())

    raise CustomError(
      status_code=500,
      message='Internal server error',
      detail='getting current infos'
    )

def get_current_positions(symbols: list = []) -> dict[float]:
  '''
  return a dict of current long positions with symbols as key
  , only if the symbol is in the portfolio
  '''

  try:
    response = requests.get(baseurl + '/positions', headers=headers)

    assert response.status_code == 200, response.json()

    response = response.json()

    if len(symbols) == 0:
      return {
        r['symbol']: {
          'qty': float(r['qty']),
          'position': r['side'],
         } for r in response
      }

    return {
      r['symbol']: {
        'qty': float(r['qty']),
        'position': r['side'],
        } for r in response if r['symbol'] in symbols
    }

  except:
    print(traceback.format_exc())

    raise CustomError(
      status_code=500,
      message='Internal server error',
      detail='getting current positions'
    )
