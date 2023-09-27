import numpy as np

from apis.alpaca.infos import get_buy_power, get_current_positions
from apis.alpaca.orders import buy_order, sell_order

def getNewPosition_Manual_v1(asset, test_end_point = 0):
  '''
  asset: asset object
  test_end_point: set to 0 for real-time judging, or set as a number larger than 0 for testing
  '''

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

def makeOrders_Manual_v1(orders):
  '''
  orders: (list of symbols to order, buy or sell orders per asset)
  '''

  symbols, sides = orders

  buy_power = get_buy_power()
  current_positions = get_current_positions()

  print('buy_power: ', buy_power)
  print('current_positions: ', current_positions)

  for i in range(len(symbols)):
    if sides[i] == 'sell':
      symbol = symbols[i]
      if symbol in current_positions:
        sell_order(symbol, current_positions[symbol])
        print('sell: ', symbol)
    else:
      buy_order(symbol, buy_power / 5)
      print('buy: ', symbol, ', buy_power: ', buy_power / 5)
      buy_power = buy_power - buy_power / 5

