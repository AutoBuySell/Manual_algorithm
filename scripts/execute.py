from apis.data.data import req_data_realtime
import traceback

from apps.error import CustomError

from scripts.core_algos.assets import Equity_Manual_v1 as ASSETCLASS
from scripts.core_algos.judge import getNewPosition_Manual_v1 as JUDGEFUNC
from scripts.core_algos.order import makeOrders_Manual_v1 as ORDERFUNC

from apis.alpaca.infos import get_current_positions
from apis.alpaca.orders import create_order

from scripts.log import create_order_log, create_error_log

def judge_and_order(OBJ_ASSETS: dict, symbols: list[str]) -> None:

  try:
    positions = get_current_positions()

    for symbol in symbols:
      if symbol not in OBJ_ASSETS:
        OBJ_ASSETS[symbol] = ASSETCLASS(symbol)
      asset = OBJ_ASSETS[symbol]

      req_data_realtime(symbol, asset.timeframe)

      if asset.check_data():
        buySig, sellSig = JUDGEFUNC(asset)
        currentPrice = asset.data['o'].iloc[-1]
        position = positions[symbol] if symbol in positions else 0

        if buySig:
          asset.update_buy_power(position)
          isOrder, qty = ORDERFUNC(asset=asset, side='buy', currentPrice=currentPrice)
          if isOrder:
            orderResults = create_order(side='buy', symbol=symbol, qty=qty)
            create_order_log(
              orderId=orderResults['orderId'],
              side='buy',
              symbol=symbol,
              qty=qty,
              price=currentPrice
            )

        elif sellSig:
          asset.update_buy_power(position)
          isOrder, qty = ORDERFUNC(asset=asset, side='sell', currentPrice=currentPrice)
          if isOrder:
            orderResults = create_order(side='sell', symbol=symbol, qty=qty)
            create_order_log(
              orderId=orderResults['orderId'],
              side='sell',
              symbol=symbol,
              qty=qty,
              price=currentPrice
            )

  except CustomError as e:
    create_error_log(traceback.format_exc())
    raise e
  except:
    print(traceback.format_exc())
    create_error_log(traceback.format_exc())

    raise CustomError(
      status_code=500,
      message='Internal server error',
      detail='judging and ordering'
    )
