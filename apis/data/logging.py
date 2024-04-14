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

def create_action_log(args: dict):
    '''
    Request to data server to create a new action log
    '''

    try:
        response = requests.post(
            url=dataServerUrl + '/logs',
            headers=headers,
            json=args,
        )

        assert response.status_code == 201, response.json()

    except:
        print(traceback.format_exc())

        raise CustomError(
            status_code=500,
            message='Internal server error',
            detail=f'creating an action log'
        )
