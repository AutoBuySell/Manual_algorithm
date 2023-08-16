import pandas as pd

import json
import os

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

        if os.path.isfile('data/setting_data/' + self.symbol + '_settings.json'):
            with open('data/setting_data/' + self.symbol + '_settings.json', 'r') as fp:
                self.settings = json.load(fp)
        else:
            print('[Warning]', self.symbol, 'has no setting files. The default settings will be used instead.')
            with open('data/setting_data/default_settings.json', 'r') as fp:
                self.settings = json.load(fp)
            self.set()

        self.check_data()

    def __repr__(self) -> str:
        return f'symbol: {self.symbol}, settings: {self.settings}.'

    def check_data(
        self,
    ) -> None:
        data_path = 'data/market_data/' + self.symbol + '_current_' + self.settings['data_interval'] + '.csv'
        if os.path.isfile(data_path):
            if self.data is not None:
                temp_data_pd = pd.read_csv(data_path)
                if temp_data_pd['Datetime'].iloc[-1] == self.data['Datetime'].iloc[-1]:
                    return False
                else:
                    self.data = temp_data_pd
                    return True
            else:
                self.data = pd.read_csv(data_path)

        return False

    def load_data(
        self,
        date: str,
    ) -> None:
        data_path = 'data/market_data/' + self.symbol + '_' + date + '_' + self.settings['data_interval'] + '.csv'
        if os.path.isfile(data_path):
            self.data = pd.read_csv(data_path)
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
                if key == 'threshold' and not 0.02 <= val <= 1:
                    self.settings[key] = 0.1
                elif key == 'duration' and val <= 0:
                    self.settings[key] = 2
                else:
                    self.settings[key] = val

        with open('data/setting_data/' + self.symbol + '_settings.json', 'w', encoding='utf-8') as fp:
            json.dump(self.settings, fp, indent='\t', ensure_ascii=False)

