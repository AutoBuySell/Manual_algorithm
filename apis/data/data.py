import requests
import os
import traceback
from dotenv import load_dotenv

from apps.error import CustomError

load_dotenv(verbose=True)

dataServerUrl = os.getenv('DATA_SERVER_URL')

headers = {
    'accept': 'application/json',
}

def req_data_realtime(symbols):
    '''
    Request to data server to update and response with updated data
    '''

    try:
      response = requests.post(
          url=dataServerUrl + '/dataArchiving/real_time',
          headers=headers,
          json={
              'symbols': symbols,
          }
      )

      assert response.status_code == 201, response.message

    except:
       print(traceback.format_exc())

       raise CustomError(
          status_code=500,
          message='Internal server error',
          detail='requesting real-data from data server'
       )