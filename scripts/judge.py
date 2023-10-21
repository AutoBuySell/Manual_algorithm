import numpy as np
import traceback

from apps.error import CustomError
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
