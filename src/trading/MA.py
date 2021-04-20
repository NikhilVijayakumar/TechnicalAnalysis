import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from tabulate import tabulate
import warnings
warnings.filterwarnings('ignore')
import pandas_datareader.data as web


def MovingAverageCrossStrategy(stockSymbol='ULTRACEMCO.NS', startDate='2018-01-01', endDate='2020-01-01',
                               shortPeriod=20, longPeriod=50, movingAverage='SMA', table=True):
    start = datetime.datetime(*map(int, startDate.split('-')))
    end = datetime.datetime(*map(int, endDate.split('-')))
    stockData = web.DataReader(stockSymbol, 'yahoo', start=start, end=end)['Close']
    stockData = pd.DataFrame(stockData)
    stockData.columns = {'Close Price'}
    stockData.dropna(axis=0, inplace=True)
    shortWindow = str(shortPeriod) + '_' + movingAverage
    longWindow = str(longPeriod) + '_' + movingAverage

    if movingAverage == 'SMA':
        stockData[shortWindow] = stockData['Close Price'].rolling(window=shortPeriod, min_periods=1).mean()
        stockData[longWindow] = stockData['Close Price'].rolling(window=longPeriod, min_periods=1).mean()

    elif movingAverage == 'EMA':

        stockData[shortWindow] = stockData['Close Price'].ewm(span=shortPeriod, adjust=False).mean()
        stockData[longWindow] = stockData['Close Price'].ewm(span=longPeriod, adjust=False).mean()


    stockData['Signal'] = 0.0
    stockData['Signal'] = np.where(stockData[shortWindow] > stockData[longWindow], 1.0, 0.0)

    stockData['Position'] = stockData['Signal'].diff()
    SMAGraph(stockData, shortWindow, longWindow, stockSymbol, movingAverage)
    if table :
        SMATable(stockData)


def SMAGraph(stockData, shortWindow, longWindow, stockSymbol, movingAverage):
    plt.figure(figsize=(20, 10))
    plt.tick_params(axis='both', labelsize=14)
    stockData['Close Price'].plot(color='k', lw=1, label='Close Price')
    stockData[shortWindow].plot(color='b', lw=1, label=shortWindow)
    stockData[longWindow].plot(color='g', lw=1, label=longWindow)

    plt.plot(stockData[stockData['Position'] == 1].index,
             stockData[shortWindow][stockData['Position'] == 1],
             '^', markersize=15, color='g', alpha=0.7, label='buy')

    plt.plot(stockData[stockData['Position'] == -1].index,
             stockData[shortWindow][stockData['Position'] == -1],
             'v', markersize=15, color='r', alpha=0.7, label='sell')
    plt.ylabel('Price in ₹', fontsize=16)
    plt.xlabel('Date', fontsize=16)
    plt.title(str(stockSymbol) + ' - ' + str(movingAverage) + ' Crossover', fontsize=20)
    plt.legend()
    plt.grid()
    plt.show()


def SMATable(stockData):
        dataPostion = stockData[(stockData['Position'] == 1) | (stockData['Position'] == -1)]
        dataPostion['Position'] = dataPostion['Position'].apply(lambda x: 'Buy' if x == 1 else 'Sell')
        print(tabulate(dataPostion, headers='keys', tablefmt='psql'))