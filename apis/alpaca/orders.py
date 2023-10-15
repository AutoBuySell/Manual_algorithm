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

    assert response.status_code == 200, response.message

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

def get_order(orderId: str) -> dict:
  '''
  특정 id 의 주문 정보 요청, 해당 주문의 status(주문상태), filledQty(실행주문수), filledAvgPrice(실행평균가) 반환
  Request order infomation of an orderId
  Return status, filledQty, filledAvgPrice infomation of the order
  '''

  try:
    response = requests.get(
      baseurl + '/orders' + f'/{orderId}',
      headers=headers
    )

    assert response.ststus_code == 200, response.message

    response = response.json()

    new_info = {
      'status': response['status'],
      'filledQty': response['filled_qty'],
      'filledAvgPrice': response['filled_avg_price'] or 0,
    }

    return new_info

  except:
    print(traceback.format_exc())

    CustomError(
      status_code=500,
      message='Internal server error',
      detail='getting an order information'
    )
