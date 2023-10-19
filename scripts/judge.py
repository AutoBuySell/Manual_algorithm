import numpy as np
from datetime import datetime
import traceback

from apps.error import CustomError

from apis.alpaca.infos import get_buy_power, get_current_positions
from apis.alpaca.orders import create_order

from scripts.log import create_order_log
from scripts.assets import Equity_Manual_v1

def getNewPosition_Manual_v1(asset: Equity_Manual_v1, test_end_point: int = 0) -> tuple[bool]:
  '''
  asset: asset object
  test_end_point: set to 0 for real-time judging, or set as a number larger than 0 for testing
  '''

  try:
    data_np = np.array(asset.data['o'])

    # For testing, use sliced data
    if test_end_point != 0:
      data_np = data_np[:test_end_point + 1]

    # The last point is the moment of judging
    current_price = data_np[-1]

    # For judging, use sliced data referred to start_point and duration
    data_np = data_np[max(-(len(data_np) - asset.start_point), -(1 + asset.settings['duration'])):-1]

    min_price = np.min(data_np)
    max_price = np.max(data_np)

    # For buying points
    thr_buy_sig_on = (1 - asset.settings['thr_buy']) * max_price >= current_price
    reb_buy_sig_on = (1 + asset.settings['rebound']) * data_np[-1] <= current_price

    # For selling points
    thr_sell_sig_on = (1 + asset.settings['thr_sell']) * min_price <= current_price
    reb_sell_sig_on = (1 - asset.settings['rebound']) * data_np[-1] >= current_price

    # If a buying or selling point has been appeared, renew test_end_point
    if (thr_buy_sig_on and reb_buy_sig_on) or (thr_sell_sig_on and reb_sell_sig_on):
      asset.start_point = len(asset.data['o']) - 2 if test_end_point == 0 else test_end_point

    return thr_buy_sig_on and reb_buy_sig_on, thr_sell_sig_on and reb_sell_sig_on

  except:
    print(traceback.format_exc())

    raise CustomError(
      status_code=500,
      message='Internal server error',
      detail='calculating new position'
    )

def makeOrders_Manual_v1(orders: tuple[list[str]], obj_assets: dict[Equity_Manual_v1]) -> None:
  '''
  orders: (list of symbols to order, list of 'buy' or 'sell' orders per asset)
  obj_assets: dict of asset objects
  '''

  try:
    symbols, sides = orders

    buy_power = get_buy_power()
    current_positions = get_current_positions()

    print(datetime.today().isoformat())
    print('buy_power: ', buy_power)
    print('current_positions: ', current_positions)
    print('new orders: ', orders)

    for i in range(len(symbols)):
      symbol = symbols[i]
      if sides[i] == 'sell':
        if symbol in current_positions:
          data_np = np.array(obj_assets[symbol].data['o'])
          current_price = data_np[-1]
          qty = current_positions[symbol]

          orderInfo = create_order('sell', symbol, qty)
          create_order_log(orderInfo['orderId'], 'sell', symbol, qty, current_price)
          print('sell: ', symbol, ', qty: ', qty, ', price: ', current_price)
      else:
        data_np = np.array(obj_assets[symbol].data['o'])
        current_price = data_np[-1]
        qty = int((buy_power / 5) / current_price)

        orderInfo = create_order('buy', symbol, qty)
        create_order_log(orderInfo['orderId'], 'buy', symbol, qty, current_price)
        print('buy: ', symbol, ', qty: ', qty, ', price: ', current_price)

        buy_power = buy_power - buy_power / 5

  except CustomError as e:
    raise e

  except:
    print(traceback.format_exc())

    raise CustomError(
      status_code=500,
      message='Internal server error',
      detail='making orders'
    )
