import json
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.graph_objects as go



def GetTypicalPrice(data, colClose='close', colHigh='high', colLow='low'):
    typicalPrice = (data[colClose] + data[colHigh] + data[colLow]) / 3
    return typicalPrice


def GetMoneyFlow(typicalPrice, df, colVolumeName):
    return typicalPrice * df[colVolumeName]

def GetPosNegMoneyFlows(typicalPrice,moneyFlow ):
    positiveFlow = []
    negativeFlow = []

    for i in range(1, len(typicalPrice)):
        if typicalPrice[i] > typicalPrice[i - 1]:
            positiveFlow.append(moneyFlow[i])
            negativeFlow.append(0)
        elif typicalPrice[i] < typicalPrice[i - 1]:
            positiveFlow.append(0)
            negativeFlow.append(moneyFlow[i])
        else:
            positiveFlow.append(0)
            negativeFlow.append(0)

    return (positiveFlow, negativeFlow)

def GetMFI(positiveFlow, negativeFlow, periodVal):
    positiveMF = []
    negativeMF = []

    for i in range(periodVal - 1, len(positiveFlow)):
        positiveMF.append(sum(positiveFlow[i + 1 - periodVal: i + 1]))

    for i in range(periodVal - 1, len(negativeFlow)):
        negativeMF.append(sum(negativeFlow[i + 1 - periodVal: i + 1]))

    mfi = 100 * (np.array(positiveMF) / (np.array(positiveMF) + np.array(negativeMF)))
    return (mfi)

def GetRSI(df, colName, periodVal):
    delta = df[colName].diff(1)
    delta = delta.dropna()

    up = delta.copy()
    down = delta.copy()

    up[up < 0] = 0
    down[down > 0] = 0

    avgGain = up.rolling(window=periodVal).mean()
    avgLoss = abs(down.rolling(window=periodVal).mean())

    rs = avgGain / avgLoss
    rsi = 100.0 - (100.0 / (1 + rs))

    rsiDf = pd.DataFrame()
    rsiDf[colName] = df[colName]
    rsiDf['rsi'] = rsi

    return (rsiDf)


def GetMfiSignals(data, high, low):
  buySignal = []
  sellSignal = []

  for i in range(len(data['MFI'])):
    if data['MFI'][i] > high:
      buySignal.append(np.nan)
      sellSignal.append(data['close'][i])
    elif data['MFI'][i] < low:
      buySignal.append(data['close'][i])
      sellSignal.append(np.nan)
    else:
      sellSignal.append(np.nan)
      buySignal.append(np.nan)

  return ( buySignal, sellSignal)



def ShowMFI(df, colName, stockName, low1=10, low2=20, high1=80, high2=90):
    plt.figure(figsize=(12.5, 4.5))
    plt.plot(df[colName], label=f'{stockName} MFI')
    plt.axhline(low1, linestyle='--', color='orange')
    plt.axhline(low2, linestyle='--', color='blue')
    plt.axhline(high1, linestyle='--', color='blue')
    plt.axhline(high2, linestyle='--', color='orange')
    plt.title(f'{stockName} MFI')
    plt.ylabel(f'{stockName}\'s MFI Values')
    plt.show()


def ShowRSI(df, colName, stockName):
    plt.figure(figsize=(12.5, 4.5))
    plt.plot(df.index, df[colName], label=f'{stockName} RSI')
    plt.axhline(0, linestyle='--', color='gray', alpha=0.5)
    plt.axhline(10, linestyle='--', color='orange', alpha=0.5)
    plt.axhline(20, linestyle='--', color='green', alpha=0.5)
    plt.axhline(30, linestyle='--', color='red', alpha=0.5)

    plt.axhline(70, linestyle='--', color='red', alpha=0.5)
    plt.axhline(80, linestyle='--', color='green', alpha=0.5)
    plt.axhline(90, linestyle='--', color='orange', alpha=0.5)
    plt.axhline(100, linestyle='--', color='gray', alpha=0.5)

    plt.title(f'{stockName} RSI')
    plt.ylabel(f'{stockName}\'s RSI Values')
    plt.show()


def ShowFigure(df, colName, stockName, titleName, xlabelName, ylabelName, legendName='upper left'):
    plt.figure(figsize=(12.5, 4.5))
    plt.plot( df.index, df[colName], label=f'{stockName} Close')
    plt.title( f'{stockName} {titleName}')
    plt.legend(df.columns.values, loc=legendName)
    plt.xlabel(xlabelName)
    plt.ylabel( f'{stockName} {ylabelName}')
    plt.show()



def ShowBuySell(df, colName, stockName, buyName, sellName, title, xlabelName, ylabelName, locName='upper left'):
    plt.figure(figsize=(12.5, 4.5))
    plt.plot(df[colName], label=f'{stockName} Close Price', alpha=0.25)
    plt.scatter(df.index, df[buyName], color='green', label='Buy', marker='^', alpha=1)
    plt.scatter(df.index, df[sellName], label='Sell', color='red', marker='v', alpha=1)

    plt.title(f'{stockName} {title}')
    plt.xlabel(xlabelName)
    plt.ylabel(ylabelName)
    plt.legend(loc=locName)
    plt.show()



def ShowCandle( pDf, pStockName ):
    figure = go.Figure(
      data = [
        go.Candlestick(
          x = pDf.index,
          low = pDf['low'],
          high = pDf['high'],
          open = pDf['open'],
          close=pDf['close'],
          increasing_line_color = 'green',
          decreasing_line_color = 'red'
        )
      ]
    )

    figure.update_layout(xaxis_rangeslider_visible =  False,
                         title = f'{pStockName} Price',
                         yaxis_title = f'{pStockName} Price in INR (Rs)',
                         xaxis_title = 'Date'
                         )
    figure.show()
