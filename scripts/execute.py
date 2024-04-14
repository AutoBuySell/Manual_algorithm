import traceback

from apps.error import CustomError

from scripts.core_algos.assets import Equity_Manual_v2 as ASSETCLASS
from scripts.core_algos.judge import getNewPosition_Manual_v2 as JUDGEFUNC
from scripts.core_algos.order import makeOrders_Manual_v2 as ORDERFUNC

from apis.data.data import req_data_realtime
from apis.data.logging import create_action_log
from apis.alpaca.orders import create_order

from scripts.log import create_error_log

def judge_and_order(OBJ_ASSETS: dict, symbols: list[str]) -> None:

  try:
    for symbol in symbols:
      if symbol not in OBJ_ASSETS:
        OBJ_ASSETS[symbol] = ASSETCLASS(symbol)
      asset = OBJ_ASSETS[symbol]

      req_data_realtime(symbol, asset.timeframe)

      if asset.check_data():
        buySig, sellSig, confidence = JUDGEFUNC(asset)
        currentPrice = asset.data['o'].iloc[-1]

        if buySig:
          create_action_log({
            'action': 'judge',
            'symbol': symbol,
            'confidence': confidence,
            'orderSide': 'buy'
          })

          isOrder, qty = ORDERFUNC(asset=asset, side='buy', confidence=confidence)
          if isOrder:
            print('buy', symbol, isOrder, qty)
            orderResults = create_order(side='buy', symbol=symbol, qty=qty)

            create_action_log({
              'action': 'order',
              'orderId': orderResults['orderId'],
              'symbol': symbol,
              'orderSide': 'buy',
              'orderQty': qty,
              'orderPrice': currentPrice,
              'orderStatus': 'new',
            })

        elif sellSig:
          create_action_log({
            'action': 'judge',
            'symbol': symbol,
            'confidence': confidence,
            'orderSide': 'sell'
          })

          isOrder, qty = ORDERFUNC(asset=asset, side='sell', confidence=confidence)
          if isOrder:
            print('sell', symbol, isOrder, qty)
            orderResults = create_order(side='sell', symbol=symbol, qty=qty)

            create_action_log({
              'action': 'order',
              'orderId': orderResults['orderId'],
              'symbol': symbol,
              'orderSide': 'sell',
              'orderQty': qty,
              'orderPrice': currentPrice,
              'orderStatus': 'new',
            })

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
