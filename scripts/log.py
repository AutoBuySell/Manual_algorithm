import os
import pandas as pd
from datetime import datetime

from apis.alpaca.orders import get_order

LOG_TEMPLATE = {
  'orderId': '',
  'date_server': '2023-01-01T00:00:00Z',
  'status': 'new',
  'symbol': 'AAPL',
  'orderQty': '1',
  'orderPrice': '1',
  'filledQty': '0',
  'filledAvgPrice': '0',
}

PATH_ORDER_LOGS = '../data/log_data/order_logs.csv'

TERMINATED_STATUS = ['filled', 'canceled', 'expired', 'rejected']

def create_order_log(orderId: str, symbol: str, qty: int, price: float):
  new_log = LOG_TEMPLATE.copy()
  new_log = {
    **new_log,
    'orderId': orderId,
    'date_server': datetime.now().isoformat(timespec='milliseconds') + 'Z',
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

def update_order_log():
  logs_pd = pd.read_csv(PATH_ORDER_LOGS)
  orderIds = logs_pd[logs_pd['status'] not in TERMINATED_STATUS]['orderId']

  for orderId in orderIds:
    new_info = get_order(orderId=orderId)

    index = logs_pd[logs_pd['orderId'] == orderId].index

    for key in new_info.keys():
      logs_pd.loc[index, key] = new_info[key]

  logs_pd.to_csv(PATH_ORDER_LOGS, index=False)

def get_order_log():
  logs_pd = pd.read_csv(PATH_ORDER_LOGS)

  return logs_pd.to_dict(orient='records')
