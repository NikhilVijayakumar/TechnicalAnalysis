import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
import warnings
warnings.filterwarnings('ignore')
from enum import Enum

class MovingAverages(str,Enum):
    SMA = "Simple Moving Average"
    EMA = "Exponential Moving Average"

class MAdata:
    def __init__(self, stockData, ticker, movingAverage=MovingAverages.SMA,shortPeriod=20, longPeriod=50):
        self.stockData = stockData
        self.ticker = ticker
        self.movingAverage = movingAverage
        self.shortPeriod = shortPeriod
        self.longPeriod = longPeriod

class MACrossover:
    def __init__(self,data):
        self.data = data
        self.shortWindow = str(data.shortPeriod) + '_' + data.movingAverage
        self.longWindow = str(data.longPeriod) + '_' + data.movingAverage


    def MovingAverageCrossStrategy(self):

        if self.data.movingAverage == MovingAverages.SMA:
            self.data.stockData[self.shortWindow] = self.data.stockData['Close'].rolling(window=self.data.shortPeriod, min_periods=1).mean()
            self.data.stockData[self.longWindow] = self.data.stockData['Close'].rolling(window=self.data.longPeriod, min_periods=1).mean()

        elif self.data.movingAverage == MovingAverages.EMA:
            self.data.stockData[self.shortWindow] = self.data.stockData['Close'].ewm(span=self.data.shortPeriod, adjust=False).mean()
            self.data.stockData[self.longWindow] = self.data.stockData['Close'].ewm(span=self.data.longPeriod, adjust=False).mean()

        self.data.stockData['Signal'] = 0.0
        self.data.stockData['Signal'] = np.where(self.data.stockData[self.data.shortWindow] > self.data.stockData[self.longWindow], 1.0, 0.0)
        self.data.stockData['Position'] = self.data.stockData['Signal'].diff()



    def MACrossoverGraph(self):
        plt.figure(figsize=(20, 10))
        plt.tick_params(axis='both', labelsize=14)
        self.data.stockData['Close'].plot(color='k', lw=1, label='Close Price')
        self.data.stockData[self.shortWindow].plot(color='b', lw=1, label=self.shortWindow)
        self.data.stockData[self.longWindow].plot(color='g', lw=1, label=self.longWindow)

        plt.plot(self.data.stockData[self.data.stockData['Position'] == 1].index,
                 self.data.stockData[self.shortWindow][self.data.stockData['Position'] == 1],
                 '^', markersize=15, color='g', alpha=0.7, label='buy')

        plt.plot(self.data.stockData[self.data.stockData['Position'] == -1].index,
                 self.data.stockData[self.shortWindow][self.data.stockData['Position'] == -1],
                 'v', markersize=15, color='r', alpha=0.7, label='sell')
        plt.ylabel('Price in ₹', fontsize=16)
        plt.xlabel('Date', fontsize=16)
        plt.title(str(self.data.ticker) + ' - ' + str(self.data.movingAverage) + ' Crossover', fontsize=20)
        plt.legend()
        plt.grid()
        plt.show()


    def MACrossoverTable(self,column = []):
        dataPostion =  self.data.stockData[( self.data.stockData['Position'] == 1) | ( self.data.stockData['Position'] == -1)]
        dataPostion['Position'] = dataPostion['Position'].apply(lambda x: 'Buy' if x == 1 else 'Sell')
        if not column:
            print(tabulate(dataPostion, headers='keys', tablefmt='psql'))
        else:
            print(tabulate(dataPostion[column], headers='keys', tablefmt='psql'))