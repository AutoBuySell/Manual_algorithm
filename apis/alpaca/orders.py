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

def create_order(side: str, symbol: str, qty: int) -> dict:
  '''
  매수 / 매도 주문 생성. 시장가로 시행함.
  Create a buy / sell order for market price

  side: 'buy' | 'sell'
  symbol: 종목코드 (stock code)
  qty: 주문 수량
  '''

  try:
    payload = {
      'side': side,
      'type': 'market',
      'time_in_force': 'day',
      'symbol': symbol,
      'qty': qty,
    }

    response = requests.post(
      baseurl + '/orders',
      json=payload,
      headers=headers
    )

    assert response.status_code == 200, response.json()

    response = response.json()

    orderInfo = {
      'orderId': response['id'],
    }

    return orderInfo

  except:
    print(traceback.format_exc())

    raise CustomError(
      status_code=500,
      message='Internal server error',
      detail=f'creating an {side}ing order'
    )
