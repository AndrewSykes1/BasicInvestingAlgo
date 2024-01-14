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

    #Stratagy 3
    days_past = ['00']
    open_price = []

    def init(self):
        
        #Stratagy 1
        #close = self.data.Close
        #self.series1 = pd.Series(close).rolling(window=self.n1).mean().values
        #self.series2 = pd.Series(close).rolling(window=self.n2).mean().values

        #Stratagy 2
        #close = self.data.Close
        #self.series1 = pd.Series(close).rolling(window=self.n1).mean().values

        #Stratagy 3
        #Nothing
    
    def next(self):

        #Stratagy 1 -> SMA crossovers: (0.5557263244638259)
        #if self.series1[-2] > self.series2[-2] and self.series1[-1] > self.series2[-2]:
        #    self.buy()
        #else:
        #    self.sell()

        #Stratagy 2 -> Price SMA Crossovers: (18.66031438424324)
        #price = self.data.Close[-1]
        #if self.series1[-1] != 'nan':
        #    if price < (.95)*self.series1[-1]:
        #        self.buy()
        #    elif price > (1.15)*self.series1[-1]:
        #        self.sell()

        #Stratagy 3 -> APA Randomness (150%)
        Close = self.data.Close
        Open = self.data.Open
        unrefined_ymd = str(self.data.index[-1])
        current_day = unrefined_ymd[8] + unrefined_ymd[9]
        
        if self.days_past[-1] == current_day:
            if self.open_price[-1][-1] >= 1.03*Open[-1]:
                self.sell()
            elif self.open_price[-1][-1] <= .95*Open:
                self.sell()
        else:
            self.days_past.append(current_day)
            self.open_price.append(Open)
            self.sell()
            self.buy()

rev = []
ticker_list = pd.read_html(
'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df = ticker_list[0]

def load_quotes(asset):
    return yf.download(asset,start='2018-01-01')

def precise_load_quotes(asset):
    return yf.download(asset,start='2023-12-04',end='2023-12-30',interval='15m')

def get_data(length=50,specify=None,ent = 'a'):
    rev = []
    if specify== None:
        pass

    elif ent == 'a':
        a = precise_load_quotes(specify)
        bt = Backtest(a,SMAcross,cash=100000,exclusive_orders=True)
        output = bt.run()
        rev.append(output['Return (Ann.) [%]'])
        bt.plot()

    else:
        a = load_quotes(specify)
        bt = Backtest(a,SMAcross,cash=100000,exclusive_orders=True)
        output = bt.run()
        rev.append(output['Return (Ann.) [%]'])

    return rev
bt.plot()
