import traceback

from apps.error import CustomError
from .assets import Equity_Manual_v1

def makeOrders_Manual_v1(asset: Equity_Manual_v1, side: str, currentPrice: float) -> tuple[bool | int]:
  '''
  orders: (list of symbols to order, list of 'buy' or 'sell' orders per asset)
  obj_assets: dict of asset objects
  '''

  try:
    isOrder = False
    qty = 0

    symbol = asset.symbol

    buy_power = asset.buy_power
    current_position = asset.current_position

    if side == 'sell' and current_position > 0:
      qty = int(current_position / 3) if current_position >= 3 else current_position
      if qty > 0:
        isOrder = True

      print('sell: ', symbol, ', qty: ', qty, ', price: ', currentPrice)

    elif side == 'buy' and buy_power > 0:
      qty = int(buy_power / 3 / currentPrice)
      if qty > 0:
        isOrder = True

      print('buy: ', symbol, ', qty: ', qty, ', price: ', currentPrice)

    return isOrder, qty

  except:
    print(traceback.format_exc())

    raise CustomError(
      status_code=500,
      message='Internal server error',
      detail='making orders'
    )
