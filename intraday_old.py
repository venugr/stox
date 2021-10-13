import pandas as pd
import time
from util import *

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    OKRED   = '\033[91m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    HIGHLIGHT= '\033[42m'



pd.set_option('display.width', 1500)
pd.set_option('display.max_rows', 1500)
pd.set_option('display.max_columns', 50)

lWb,lLoginList, lErr=GetLogin('/Users/venul/PycharmProjects/pythonProject1/venv/AutoTrade/samco.xlsx')

if lErr != None:
    print(lErr)
    sys.exit(1)

if lLoginList[3] == "":
    DoSamcoLogin(lWb, lLoginList)

lSymName, lErr = GetIntradaySym('/Users/venul/PycharmProjects/pythonProject1/venv/AutoTrade/samco.xlsx')
if lErr != None:
    print(lErr)
    sys.exit(1)

print(lSymName)



lData, lErr = GetCandleData(lLoginList[3], lSymName, None, '09:00:00', '15', '09:45:00')

if lErr != None:
    print(lErr)
    sys.exit(1)

print(lData)

df = pd.DataFrame(lData['intradayCandleData'])
df = df.set_index(pd.DatetimeIndex(df['dateTime']))
df['low'] = pd.to_numeric(df['low'])
df['high'] = pd.to_numeric(df['high'])
print(df)
# print(type(df['low'][2]))

highAt930=None
lowAt930=None
diff930=None

if len(df['low']) >=2:
   highAt930=df['high'][2]
   lowAt930=df['low'][2]
   diff930 = (highAt930 - lowAt930)/1.0
   print("High @9:45= ", highAt930)
   print("Low @9:45= ", lowAt930)


lData, lErr = GetCandleData(lLoginList[3], lSymName, None, '09:45:00', '1')

if lErr != None:
    print(lErr)
    sys.exit(1)

print(lData)

df = pd.DataFrame(lData['intradayCandleData'])
df = df.set_index(pd.DatetimeIndex(df['dateTime']))
df['low'] = pd.to_numeric(df['low'])
df['high'] = pd.to_numeric(df['high'])
print(df)
# print(type(df['low'][2]))
lBought = False
lSold = False
lTarget = 0
lTxt = ""
lNumOfShare = 100
lNoTradeToday = False
lTrailStopLossSet = False
lTrailStopLoss = 0
lTrailStopLossHit = False
lOkForStopLoss = True
lBoughtPrice = 0


print("\n\n" + lSymName)
for i in range(len(df['high'])):

    if lTrailStopLossHit:
        break

    lTxt = df["dateTime"][i] + " - " + str(df['high'][i]) + " - " + str(df['low'][i])
    lLTPH = df['high'][i]
    lLTPL = df['low'][i]
    lPrint = False
    if lLTPH > highAt930 and not lBought:
        lTxt = lTxt + "   \t" + "**** BUY" + " (High: " + str(highAt930) + ", Low: " + str(lowAt930) +")"
        lTxt = lTxt + " - Diff.Amm: " + str(lLTPH - lowAt930) + " - Buy Price: " + str(lLTPH)
        lBought = True
        lPrint = True
        lBoughtPrice = lLTPH
        lNoTradeToday = True
        lTrailStopLoss = lowAt930

    if lBought and (lLTPH < lBoughtPrice):
        lTxt = lTxt + '   \t' + bcolors.WARNING + "**** IN LOSS"
        lTxt = lTxt + " (High: " + str(highAt930) + ", Low: " + str(lowAt930) + ")"
        lTxt = lTxt + " - Diff.Amm: " + str(lBoughtPrice - lLTPL)
        lTxt = lTxt + " - Loss: " + str(lNumOfShare * (lBoughtPrice - lLTPL))
        lTxt = lTxt + bcolors.ENDC
        lPrint = True

    if lLTPL < lowAt930 and (not lSold and lBought):
        lTxt = lTxt + '   \t' + bcolors.BOLD + bcolors.OKRED + "**** LOSS SELL"
        lTxt = lTxt + " (High: " + str(highAt930) + ", Low: " + str(lowAt930) +")"
        lTxt = lTxt + " - Diff.Amm: " + str(lBoughtPrice - lLTPL)
        lTxt = lTxt + " - Loss: " + str(lNumOfShare * (lBoughtPrice - lLTPL))
        lTxt = lTxt + bcolors.ENDC
        lSold = True
        lBought = False
        lPrint = True


    if (lLTPH - lBoughtPrice) >= diff930 and lBought:
        lTarget += 1
        lDiffStopLoss = diff930
        diff930 = 2 * diff930
        lPrint = True
        lTrailStopLossSet = True
        if lOkForStopLoss:
            lTrailStopLoss = lLTPH - (lDiffStopLoss / 1.0)

        lTxt = lTxt + '   \t' + bcolors.BOLD + bcolors.OKGREEN + '**** TARGET SELL: ' + str(lTarget)
        lTxt = lTxt + ' - Trail SL to: ' + str(lTrailStopLoss) + " - Sell Price: " + str(lLTPH)
        lTxt = lTxt + " - Diff.Amm: " + str(lLTPH - lBoughtPrice)
        lTxt = lTxt + " - GAIN: " + str(lNumOfShare * (lLTPH - lBoughtPrice))
        lTxt = lTxt + bcolors.ENDC

    if lBought and ( i == (len(df['high']) -1 )):
        lTxt = lTxt + '   \t' + bcolors.BOLD + bcolors.HIGHLIGHT + '**** IF SELL(NOW): '
        lTxt = lTxt + ' - Trail SL to: ' + str(lTrailStopLoss) + " - Sell Price: " + str(lLTPH)
        lTxt = lTxt + " - Diff.Amm: " + str(lLTPH - lBoughtPrice)
        lTxt = lTxt + " - GAIN/LOSS: " + str(lNumOfShare * (lLTPH - lBoughtPrice))
        lTxt = lTxt + bcolors.ENDC
        print(lTxt)

    if lBought and (lLTPH < lTrailStopLoss):
        lTarget += 1
        lTxt = lTxt + '   \t' + bcolors.BOLD + bcolors.OKGREEN + '**** Trail SL HIT: ' + str(lTarget)
        lTxt = lTxt + " (High: " + str(highAt930) + ", Low: " + str(lowAt930) + ")"
        lTxt = lTxt + " - Diff.Amm: " + str(lTrailStopLoss - lBoughtPrice)
        lTxt = lTxt + " - GAIN: " + str(lNumOfShare * (lTrailStopLoss - lBoughtPrice))
        lTxt = lTxt + bcolors.ENDC
        lPrint = True
        lTrailStopLossHit = True
        lSold = True
        lBought = False


    if lBought and ("15:00:00" in df["dateTime"][i]):
        lTarget += 1
        lDiffAmm = lLTPH - lBoughtPrice
        lColor = bcolors.OKGREEN
        if lDiffAmm <= 0:
            lColor = bcolors.OKRED

        lTxt = lTxt + '   \t' + bcolors.BOLD + lColor + '**** FINAL TARGET SELL: ' + str(lTarget)
        lTxt = lTxt + " - (High: " + str(highAt930) + ", Low: " + str(lowAt930) + ")"
        lTxt = lTxt + " - Diff.Amm: " + str(lDiffAmm)
        lTxt = lTxt + " - GAIN/LOSS: " + str(lNumOfShare * (lLTPH - lBoughtPrice))
        lTxt = lTxt + bcolors.ENDC
        diff930 = 2 * diff930
        lPrint = True

    if lPrint:
        print(lTxt)

    # time.sleep(0.01)

if not lNoTradeToday:
    lTxt = '\t' + bcolors.BOLD + bcolors.OKRED + '**** NO TRADE POSSIBLE TODAY **** '
    lTxt = lTxt + bcolors.ENDC
    print(lTxt)

# lRepeat = 5
#
# print(f'Fetching  Data...{lSymName}')
# lBought = False
# lSold = False
#
# while (True):
#     # print('-' * 30)
#     lData, lErr = GetQuote(lLoginList, lSymName)
#
#     if lErr != None:
#         print(lErr)
#         sys.exit(1)
#     # print(lData)
#     # print(lData["lastTradedTime"] + " - " + lData["lastTradedPrice"])
#     lTxt = lData["lastTradedTime"] + " - " + lData["lastTradedPrice"]
#
#     lLTP = float(lData["lastTradedPrice"])
#     if lLTP > highAt930 and not lBought:
#         lTxt = lTxt + " " + "BUY"
#         lBought = True
#
#     if lLTP < lowAt930 and not lSold:
#         lTxt = lTxt + ' ' + "SELL"
#         lSold = True
#
#     print(lTxt)
#     time.sleep(lRepeat)