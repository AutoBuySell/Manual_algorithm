import os
import pandas as pd
from datetime import datetime
import traceback

from apps.error import CustomError

from apis.alpaca.orders import get_order

LOG_TEMPLATE = {
  'orderId': '',
  'date_server': '2023-01-01T00:00:00Z',
  'side': '',
  'status': 'new',
  'symbol': 'AAPL',
  'orderQty': '1',
  'orderPrice': '1',
  'filledQty': '0',
  'filledAvgPrice': '0',
}

PATH_ORDER_LOGS = '../data/log_data/order_logs.csv'
PATH_ERROR_LOGS = '../data/log_data/error_logs.csv'

TERMINATED_STATUS = ['filled', 'canceled', 'expired', 'rejected', 'closed']

def create_order_log(orderId: str, side: str, symbol: str, qty: int, price: float) -> None:
  '''
  Create a line of order log when an order occured.
  '''

  try:
    new_log = LOG_TEMPLATE.copy()
    new_log = {
      **new_log,
      'orderId': orderId,
      'date_server': datetime.now().isoformat(timespec='milliseconds') + 'Z',
      'side': side,
      'symbol': symbol,
      'orderQty': qty,
      'orderPrice': price,
    }

    if os.path.isfile(PATH_ORDER_LOGS):
      logs_pd = pd.read_csv(PATH_ORDER_LOGS)
      logs_pd = pd.concat([logs_pd, pd.DataFrame(new_log, index=[0])], ignore_index=True)
    else:
      logs_pd = pd.DataFrame(new_log, index=[0])

    logs_pd.to_csv(PATH_ORDER_LOGS, index=False)

  except:
    print(traceback.format_exc())

    raise CustomError(
      status_code=500,
      message='Internal server error',
      detail='creating an order log'
    )

def update_order_log():
  '''
  Update lines of order logs which are not in terminated status
  '''

  try:
    logs_pd = pd.read_csv(PATH_ORDER_LOGS)
    orderIds = logs_pd[~logs_pd['status'].isin(TERMINATED_STATUS)]['orderId']

    for orderId in orderIds:
      new_info = get_order(orderId=orderId)

      index = logs_pd[logs_pd['orderId'] == orderId].index

      for key in new_info.keys():
        logs_pd.loc[index, key] = new_info[key]

    logs_pd.to_csv(PATH_ORDER_LOGS, index=False)

  except:
    print(traceback.format_exc())

    raise CustomError(
      status_code=500,
      message='Internal server error',
      detail='updating order logs'
    )

def get_order_log():
  '''
  Get all of the order logs stored currently
  '''

  try:
    logs_pd = pd.read_csv(PATH_ORDER_LOGS)

    return logs_pd.to_dict(orient='records')

  except:
    print(traceback.format_exc())

    raise CustomError(
      status_code=500,
      message='Internal server error',
      detail='getting all order logs'
    )

def create_error_log(content: str) -> None:
  '''
  Create a line of error log when an error occured.
  '''

  try:
    new_log = {
      'date': datetime.now().isoformat(timespec='milliseconds') + 'Z',
      'content': content
    }

    if os.path.isfile(PATH_ERROR_LOGS):
      logs_pd = pd.read_csv(PATH_ERROR_LOGS)
      logs_pd = pd.concat([logs_pd, pd.DataFrame(new_log, index=[0])], ignore_index=True)
    else:
      logs_pd = pd.DataFrame(new_log, index=[0])

    logs_pd.to_csv(PATH_ERROR_LOGS, index=False)

  except:
    print(traceback.format_exc())

    raise CustomError(
      status_code=500,
      message='Internal server error',
      detail='creating an error log'
    )
