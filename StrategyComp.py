import yfinance as yf
import ta
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG
import inspect

class SMAcross(Strategy):

    #Stratagy 1
    n1 = 50
    n2 = 100

    #Stratagy 2
    n1 = 50

    def init(self):
        
        #Stratagy 1
        close = self.data.Close
        self.series1 = pd.Series(close).rolling(window=self.n1).mean().values
        self.series2 = pd.Series(close).rolling(window=self.n2).mean().values

        #Stratagy 2
        #close = self.data.Close
        #self.series1 = pd.Series(close).rolling(window=self.n1).mean().values
    
    def next(self):

        #Stratagy 1 -> SMA crossovers: (0.5557263244638259)
        if self.series1[-2] > self.series2[-2] and self.series1[-1] > self.series2[-2]:
            self.buy()
        else:
            self.sell()

        #Stratagy 2 -> Price SMA Crossovers: (18.66031438424324)
        #price = self.data.Close[-1]
        #if self.series1[-1] != 'nan':
        #    if price < (.95)*self.series1[-1]:
        #        self.buy()
        #    elif price > (1.15)*self.series1[-1]:
        #        self.sell()

        #If price < (.95)20W avg -> Buy
        #If price > (1.05)20W avg -> Sell

rev = []
ticker_list = pd.read_html(
'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df = ticker_list[0]

def load_quotes(asset):
    return yf.download(asset,start='2018-01-01')
for i in range(500):
    if type(df['Symbol'][i]) == str:
        a = load_quotes(df['Symbol'][i])
        try:
            bt = Backtest(a,SMAcross,cash=100000,exclusive_orders=True)
        except ValueError:
            continue
        output = bt.run()
        rev.append(output['Return (Ann.) [%]'])
    if i % 40 == 0:
        print(i)

bt.plot()
