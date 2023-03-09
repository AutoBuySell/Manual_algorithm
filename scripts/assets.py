from pathlib import Path
import glob
import pandas as pd
import datetime

class Equity():
    '''
    Equity class has its own history and properties for deciding to open or close positions of a specific stock.

    - parameters
    symbol: (ticker) alphabet abbreviation for a specific stock
    threshold: minimum percentage of value change to decide buy or sell
    duration: minimum duration of consistency of value change to decide buy or sell
    rebound: gradient of change as a trigger of action
    limit: maximum amount of total value per action
    '''
    def __init__(
        self,
        symbol: str,
        threshold: float = 0.1,
        duration: int = 2,
        thr_grad: float = 0.02,
        rebound: float = 0,
        limit: int = 1000,
    ) -> None:
        if not (0.02 <= threshold <= 1):
            threshold = 0.1
        if duration <= 0:
            duration = 2
        self.symbol = symbol
        self.thr_buy = threshold
        self.thr_sell = threshold
        self.dur = duration
        self.thr_grad = thr_grad
        self.reb = rebound
        self.limit = limit

    def __repr__(self) -> str:
        return f'symbol: {self.symbol}, thresholds: {self.thr_buy, self.thr_sell}, duration: {self.dur}, gradient_threshold: {self.thr_grad}, rebound: {self.reb}, limit: {self.limit}.'

    def load(
        self,
        path: Path or str
    ) -> None:
        '''
        load settings of a specific stock from given path
        if multiple settings exist, load the most recent one

        - parameters
        path: relative or absolute path of source folder
        '''
        if isinstance(path, str):
            path = Path(path)

        recent_docs = glob.glob(str(path) + '/' + self.symbol + '_*_settings.csv')
        if recent_docs:
            setting = pd.read_csv(recent_docs[-1], sep=',')
            self.thr_buy = setting['thr_buy'].iloc[-1]
            self.thr_sell = setting['thr_sell'].iloc[-1]
            self.dur = setting['duration'].iloc[-1]
            self.thr_grad = setting['thr_grad'].iloc[-1]
            self.reb = setting['rebound'].iloc[-1]
            self.limit = setting['limit'].iloc[-1]

    def save(
        self,
        path: Path or str
    ) -> None:
        '''
        save settings of a specific stock to given path
        saved date is recorded at file name

        - parameters
        path: relative or absolute path of target folder
        '''
        if isinstance(path, str):
            path = Path(path)

        today = datetime.datetime.now()
        filewritingdate = today.strftime('%y') + today.strftime('%m') + today.strftime('%d')

        new_setting = pd.DataFrame(
            [[self.thr_buy, self.thr_sell, self.dur, self.thr_grad, self.reb, self.limit]],
            columns=['thr_buy', 'thr_sell', 'duration', 'thr_grad', 'rebound', 'limit']
        )

        prev_docs = glob.glob(str(path) + '/' + self.symbol + f'_{filewritingdate}_settings.csv')

        if prev_docs:
            setting = pd.read_csv(prev_docs[-1], sep=',', index_col=0)
            new_setting = pd.concat([setting, new_setting])

        new_setting.to_csv(str(path) + '/' + self.symbol + f'_{filewritingdate}_settings.csv', sep=',')
