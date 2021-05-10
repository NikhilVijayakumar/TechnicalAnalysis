import pandas as pd
import pandas_datareader.data as web


class TestData:
    def __init__(self, ticker, start,end):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.ge = None
        self.apple = None
        self.ultratech = None
        self.ms = None
        self.generateData()

    def generateData(self):
        df = web.DataReader(name=self.ticker, data_source="yahoo", start=self.start, end=self.end)
        df.to_csv("TestData.csv")
        df = pd.read_csv("TestData.csv", header=[0, 1], index_col=0, parse_dates=[0])
        self.ge = df.swaplevel(axis=1).GE.copy()
        self.ms = df.swaplevel(axis=1).MSFT.copy()
        self.apple = df.swaplevel(axis=1).AAPL.copy()
        data = df.swaplevel(axis=1)
        self.ultratech = data["ULTRACEMCO.NS"].copy()





ticker = ["MSFT","GE","AAPL","ULTRACEMCO.NS"]
start = "01-01-2018"
end = "31-12-2020"
data = TestData(ticker, start,end)

print(data.ge)



