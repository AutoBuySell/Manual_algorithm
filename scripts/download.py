import yfinance as yf
import pandas as pd
import datetime

def download1mdata(symbol):
    today = datetime.datetime.now()
    filewritingdate = today.strftime('%y') + today.strftime('%m') + today.strftime('%d')

    data = yf.download(
        tickers=symbol,
        period='max',
        interval='1m'
    )
    data = pd.DataFrame(data)

    pd.DataFrame.to_csv(data, f'./data/market_data/{symbol}_{filewritingdate}_1m.csv', sep=',')
    print(f'Saved {symbol} 1 minute interval data.')

def download5mdata(symbol):
    today = datetime.datetime.now()
    startdate = today - datetime.timedelta(days=30)
    filewritingdate = today.strftime('%y') + today.strftime('%m') + today.strftime('%d')

    data = yf.download(
        tickers=symbol,
        start=f"{startdate.strftime('%Y')}-{startdate.strftime('%m')}-{startdate.strftime('%d')}",
        end=f"{today.strftime('%Y')}-{today.strftime('%m')}-{today.strftime('%d')}",
        interval='5m'
    )
    data = pd.DataFrame(data)

    pd.DataFrame.to_csv(data, f'./data/market_data/{symbol}_{filewritingdate}_5m.csv', sep=',')
    print(f'Saved {symbol} 5 minute interval data.')

def updateShortPeriodData():
  target_company = pd.read_csv('./data/target_company.csv', sep=',')
  print('Downloading all listed data')
  for i in range(len(target_company)):
      sb = target_company['Symbol'][i]
      download5mdata(sb)
      download1mdata(sb)
  print('Done')
