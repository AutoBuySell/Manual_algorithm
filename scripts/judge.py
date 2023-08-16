import numpy as np

def get_new_position(asset, test_end_point = 0):
  data_np = np.array(asset.data['Open'])

  if test_end_point != 0:
    data_np = data_np[:test_end_point + 1]

  current_price = data_np[-1]

  data_np = data_np[max(-(len(data_np) - asset.start_point), -(1 + asset.settings['duration'])):-1]

  min_price = np.min(data_np)
  max_price = np.max(data_np)

  thr_buy_sig_on = (1 - asset.settings['thr_buy']) * max_price >= current_price
  reb_buy_sig_on = (1 + asset.settings['rebound']) * data_np[-1] <= current_price
  thr_sell_sig_on = (1 + asset.settings['thr_sell']) * min_price <= current_price
  reb_sell_sig_on = (1 - asset.settings['rebound']) * data_np[-1] >= current_price

  if (thr_buy_sig_on and reb_buy_sig_on) or (thr_sell_sig_on and reb_sell_sig_on):
    asset.start_point = len(asset.data['Open']) - 2

  return thr_buy_sig_on and reb_buy_sig_on, thr_sell_sig_on and reb_sell_sig_on
