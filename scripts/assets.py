import pandas as pd

import json
import os

PATH_MARKET_DATA = '../data/market_data/'
PATH_SETTING_DATA = '../data/setting_data/'
PATH_DEFAULT_SETTING = 'configs/default_settings.json'

class Equity_Manual_v1():
    '''
    Equity class has its own history and properties for deciding to open or close positions of a specific stock.

    - parameters
    symbol: (ticker) alphabet abbreviation for a specific stock
    settings:
        threshold: minimum percentage of value change to decide buy or sell
        duration: minimum duration of consistency of value change to decide buy or sell
        thr_grad: minimum average of gradient to decide buy or sell
        rebound: gradient of change as a trigger of action
        limit: maximum amount of total value per action
    '''
    def __init__(
        self,
        symbol: str,
    ) -> None:
        self.symbol = symbol
        self.data = None
        self.start_point = 0

        self.data_path = PATH_MARKET_DATA + self.symbol + '.csv'

        if os.path.isfile(PATH_SETTING_DATA + self.symbol + '_settings.json'):
            with open(PATH_SETTING_DATA + self.symbol + '_settings.json', 'r') as fp:
                self.settings = json.load(fp)
        else:
            print('[Warning]', self.symbol, 'has no setting files. The default settings will be used instead.')
            with open(PATH_DEFAULT_SETTING, 'r') as fp:
                self.settings = json.load(fp)['default']
            self.set()

        self.load_data() # Initialize self.data

    def __repr__(self) -> str:
        return '{' + f'symbol: {self.symbol}, settings: {self.settings}' + '}'

    def check_data(
        self,
    ) -> None:
        if os.path.isfile(self.data_path):
            if self.data is not None:
                temp_data_pd = pd.read_csv(self.data_path)
                if temp_data_pd['t'].iloc[-1] == self.data['t'].iloc[-1]:
                    return False
                else:
                    self.data = temp_data_pd
                    return True
            else:
                self.data = pd.read_csv(self.data_path)

        return False

    def load_data(
        self,
    ) -> None:
        if os.path.isfile(self.data_path):
            self.data = pd.read_csv(self.data_path)
        else:
            self.data = None
            print('No data available!')

        self.start_point = 0

    def set(
        self,
        **args,
    ) -> None:
        for key, val in args.items():
            if key in self.settings:
                self.settings[key] = val

        with open(PATH_SETTING_DATA + self.symbol + '_settings.json', 'w', encoding='utf-8') as fp:
            json.dump(self.settings, fp, indent='\t', ensure_ascii=False)

def get_default_settings():
    with open(PATH_DEFAULT_SETTING, 'r') as fp:
        settings = json.load(fp)

    return settings
