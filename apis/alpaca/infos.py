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

def get_buy_power() -> float:
  '''
  return current buy power
  '''

  try:
    response = requests.get(baseurl + '/account', headers=headers)

    assert response.status_code == 200, response.message

    response = response.json()

    return float(response['buying_power'])

  except:
    print(traceback.format_exc())

    raise CustomError(
      status_code=500,
      message='Internal server error',
      detail='getting current buying power'
    )

def get_current_positions() -> dict[float]:
  '''
  return a dict of current long positions with symbols as key
  '''

  try:
    response = requests.get(baseurl + '/positions', headers=headers)

    assert response.status_code == 200, response.message

    response = response.json()

    return {r['symbol']: float(r['qty']) for r in response if r['side'] == 'long'}

  except:
    print(traceback.format_exc())

    raise CustomError(
      status_code=500,
      message='Internal server error',
      detail='getting current positions'
    )
