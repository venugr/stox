import yfinance as yf
import sys
import pandas as pd
import time
from util import *
import datetime as dt
from intraday_stox import *

pd.set_option('display.width', 1500)
pd.set_option('display.max_rows', 1500)
pd.set_option('display.max_columns', 50)

stox = "IRCTC.NS"

# yfIntraday = yf.download('SBIN.NS', start='2021-10-11', end='2021-10-12', interval="1m")
yfIntraday = yf.download(stox, start='2021-10-12', interval="1m")
# print(yfIntraday)



def Intradaytrend( df, entry, exit):
    ret_120min = df.iloc[120].Open /df.iloc[0].Open - 1
    print(ret_120min)

    tickret = df.Open.pct_change()
    # print(tickret)

    if ret_120min > entry:
        buyprice = df.iloc[121].Open
        buytime  = df.iloc[121].name
        print( "Buy Price/Time:", buyprice, buytime)
        cumulated = (tickret.loc[buytime:] + 1).cumprod() - 1
        print(cumulated)

        exittime = cumulated[(cumulated < -exit) | (cumulated > exit)].first_valid_index()
        print(exittime)

        if exittime == None:
            exitprice = df.iloc[-1].Open
        else:
            exitprice = df.loc[exittime + dt.timedelta(minutes=1)].Open

        print("Buy  Time/Price:", buytime,  buyprice)
        print("Exit Time/Price:", exittime, exitprice)

        profit = exitprice - buyprice
        print("Profit:", profit)

        relativeProfit = profit/buyprice
        print("Relative Profit:", relativeProfit)

        return relativeProfit
    else:
        return None




Intradaytrend(yfIntraday, 0.01, 0.02)

toDay = getDate("yyyy-mm-dd")
print(toDay)

pastDay = getDate("yyyy-mm-dd", datetime.datetime.now() - dt.timedelta(days=30))
print(pastDay)

datesframe = yf.download(stox, start=pastDay, end=toDay)
print(datesframe.index)

frames = []
for i in datesframe.index:
    frames.append( yf.download(stox, start=i, end= i + dt.timedelta(days=1), interval="1m"))

returns = []

for i in frames:
    returns.append(Intradaytrend(i, 0.01, 0.02))

print(returns)

print("Mean:", pd.DataFrame(returns).mean())