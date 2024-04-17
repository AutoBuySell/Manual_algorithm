import os
import pandas as pd
from datetime import datetime
import traceback

from apps.error import CustomError

PATH_ERROR_LOGS = '../data/log_data/backend_server_error_logs.csv'

def create_error_log(content: str) -> None:
  '''
  Create a line of error log when an error occured.
  '''

  try:
    new_log = {
      'date': datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
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
