import json
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from util_plot import *
plt.style.use('fivethirtyeight')

stockName='infy'
stockNameUp=stockName.upper()

mystock=pd.read_json(f"{stockName}.json")
#mystock['close']

# plt.figure(figsize=(12.5,4.5))
# plt.plot(mystock['close'], label='INFOSYS')
# plt.title('SBI Close Price History')
# plt.xlabel('Jan. 01, 2017 - Aug. 31, 2021 ')
# plt.ylabel('Close Price in INR(Rs)')
# plt.legend(loc="upper left")
# plt.show()

sma30=pd.DataFrame()
sma30['close'] = mystock['close'].rolling(window=30).mean()

sma100=pd.DataFrame()
sma100['close'] = mystock['close'].rolling(window=100).mean()

# plt.figure(figsize=(12.5,4.5))
# plt.plot(mystock['close'], label=stockNameUp)
# plt.plot(sma30['close'], label='SMA30')
# plt.plot(sma100['close'], label='SMA100')
# plt.title(f'{stockNameUp} Close Price History')
# plt.xlabel('Jan. 01, 2019 - Aug. 31, 2021 ')
# plt.ylabel('Close Price in INR(Rs)')
# plt.legend(loc="upper left")
# plt.show()


data = pd.DataFrame()
data[stockNameUp] = mystock['close']
data['SMA30'] = sma30['close']
data['SMA100'] = sma100['close']


def buySell(data, stockNameUp ):
  sigPriceBuy = []
  sigPriceSell = []
  flag = -1

  for i in range(len(data)):
    if data['SMA30'][i] > data['SMA100'][i]:
      if flag != 1:
        sigPriceBuy.append(data[stockNameUp][i])
        sigPriceSell.append(np.nan)
        flag = 1
      else:
        sigPriceBuy.append(np.nan)
        sigPriceSell.append(np.nan)
    elif data['SMA30'][i] < data['SMA100'][i]:
      if flag != 0:
        sigPriceBuy.append(np.nan)
        sigPriceSell.append(data[stockNameUp][i])
        flag = 0
      else:
        sigPriceBuy.append(np.nan)
        sigPriceSell.append(np.nan)
    else:
      sigPriceBuy.append(np.nan)
      sigPriceSell.append(np.nan)

  return (sigPriceBuy, sigPriceSell)


buy_sell= buySell(data, stockNameUp)
data['Buy_Signal_Price'] = buy_sell[0]
data['Sell_Signal_Price'] = buy_sell[1]

plt.figure(figsize=(12.5,4.5))
plt.plot(data[stockNameUp], label=stockNameUp, alpha=0.30)
plt.plot(data['SMA30'], label='SMA30', alpha=0.30)
plt.plot(data['SMA100'], label='SMA100', alpha=0.30)
plt.scatter(data.index, data['Buy_Signal_Price'], label='Buy', marker='^', color='green' )
plt.scatter(data.index, data['Sell_Signal_Price'], label='Sell', marker='v', color='red' )

plt.title(f'{stockNameUp} Close Price History Buy & Sell Signals')
plt.xlabel('Jan. 01, 2019 - Aug. 31, 2021 ')
plt.ylabel('Close Price in INR(Rs)')
plt.legend(loc="upper left")
###plt.show()

startIdx = len(mystock) - 50
df = mystock[startIdx:]
df = df.set_index(pd.DatetimeIndex(df['date'].values))
print(df)
ShortEMA = df.close.ewm(span=12, adjust=False).mean()
LongEMA = df.close.ewm(span=26, adjust=False).mean()
MACD = ShortEMA - LongEMA
signal = MACD.ewm(span=9, adjust=False).mean()

plt.figure(figsize=(12.5,4.5))
plt.plot(df.index, MACD, label=f'{stockNameUp} MACD', color='red')
plt.plot(df.index, signal, label=f'{stockNameUp} Signal Line', color='blue')
plt.title(f'{stockNameUp} MACD/Signal')
plt.xticks(rotation=45)
# plt.xlabel('Date')
# plt.ylabel('Price in INR (Rs)')
plt.legend(loc='upper left')
###plt.show()

df['MACD'] = MACD
df['Signal'] = signal

def buy_sell(signal):
  buy=[]
  sell=[]
  flag = -1

  for i in range(0, len(signal)):
    if signal['MACD'][i] > signal['Signal'][i]:
      sell.append(np.nan)
      if flag != 1:
        buy.append(signal['close'][i])
        flag = 1
      else:
        buy.append(np.nan)
    elif signal['MACD'][i] < signal['Signal'][i]:
      buy.append(np.nan)
      if flag != 0:
        sell.append(signal['close'][i])
        flag = 0
      else:
        sell.append(np.nan)
    else:
      sell.append(np.nan)
      buy.append(np.nan)

  return (buy, sell)

a = buy_sell(df)
df['Buy_Signal_Price'] = a[0]
df['Sell_Signal_Price'] = a[1]

plt.figure(figsize=(12.5,4.5))
plt.scatter(df.index, df['Buy_Signal_Price'], color='green', label='Buy',  marker='^', alpha=1)
plt.scatter(df.index, df['Sell_Signal_Price'], label='Sell', color='red', marker='v', alpha=1)
plt.plot(df['close'], label=f'{stockNameUp} Close Price', alpha=0.25)
plt.title(f'{stockNameUp} Close Price Buy & Sell Signal')
plt.xticks(rotation=45)
plt.xlabel('Date')
plt.ylabel('Price in INR (Rs)')
plt.legend(loc='upper left')
##plt.show()


import plotly.graph_objects as go
# figure = go.Figure(
#   data = [
#     go.Candlestick(
#       x = df.index,
#       low = df['low'],
#       high = df['high'],
#       open = df['open'],
#       close=df['close'],
#       increasing_line_color = 'green',
#       decreasing_line_color = 'red'
#     )
#   ]
# )
#
# figure.update_layout(xaxis_rangeslider_visible =  False,
#                      title = f'{stockNameUp} Price',
#                      yaxis_title = f'{stockNameUp} Price in INR (Rs)',
#                      xaxis_title = 'Date'
#                      )
# figure.show()
###ShowCandle(df,stockNameUp )



typicalPrice = GetTypicalPrice(df)
moneyFlow = GetMoneyFlow(typicalPrice, df, 'volume')
(positiveFlow, negativeFlow) = GetPosNegMoneyFlows( typicalPrice, moneyFlow)

periodVal = 14
mfi = GetMFI(positiveFlow, negativeFlow, periodVal)

pd.set_option('mode.chained_assignment', None)
df2 = pd.DataFrame()
df2['MFI'] = mfi
ShowMFI(df2, 'MFI', stockNameUp)


new_df = pd.DataFrame()
new_df = df[periodVal:]
new_df['MFI'] = mfi
# print( new_df)

(new_df['Buy'], new_df['Sell']) = GetMfiSignals(new_df, 80, 20)
print(new_df)
ShowBuySell(new_df, 'close', stockNameUp, 'Buy', 'Sell',
            'Close Price Buy & Sell Signal using MFI',
            'Date','Price in INR(Rs)')


###################RSI###################
# delta = df['close'].diff(1)
# delta = delta.dropna()
# # print(delta)
#
# up = delta.copy()
# down = delta.copy()
#
# up[up < 0 ] = 0
# down [ down > 0 ] = 0
#
# # print(up)
# # print(down)
#
# periodVal = 14
# avgGain = up.rolling(window=periodVal).mean()
# avgLoss = abs(down.rolling(window=periodVal).mean())
# # print ( avgLoss, avgGain)
#
# rs = avgGain /avgLoss
# rsi = 100.0 - ( 100.0 / ( 1 + rs))
# plt.figure(figsize=(12.5,4.5))
# rsi.plot()
# plt.show()
#
# new_df = pd.DataFrame()
# new_df['close'] = df['close']
# new_df['rsi'] = rsi
# print(new_df)

new_df = GetRSI(df, 'close', 14)

ShowFigure(new_df, 'close', stockNameUp, 'Close Price History', 'Date', 'Close Price in INR(Rs)')
ShowRSI(new_df, 'rsi', stockNameUp)
