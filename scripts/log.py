import os
import pandas as pd
from datetime import datetime

LOG_TEMPLATE = {
  'orderNumber': '',
  'date_server': '2023-01-01T00:00:00Z',
  'status': 'open',
  'symbol': 'TSLA',
  'orderQty': 1,
  'orderPrice': 1,
  'filledQty': 0,
  'filledAvgPrice': 0,
}

PATH_ORDER_LOGS = '../data/log_data/order_logs.csv'

def create_order_log(orderNumber: str, symbol: str, qty: int, price: float):
  new_log = LOG_TEMPLATE.copy()
  new_log = {
    **new_log,
    'orderNumber': orderNumber,
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
  pass
