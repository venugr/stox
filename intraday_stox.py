import sys
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

def ProcessCandleDataFor930(sessionId, stockName, lJson, lWb):
    df = pd.DataFrame(lJson['intradayCandleData'])
    df = df.set_index(pd.DatetimeIndex(df['dateTime']))
    df['low'] = pd.to_numeric(df['low'])
    df['high'] = pd.to_numeric(df['high'])

    highAt930 = None
    lowAt930 = None
    diff930 = None
    lErr = None

    if len(df['low']) >= 3:
        highAt930 = df['high'][2]
        lowAt930 = df['low'][2]
        diff930 = (highAt930 - lowAt930) / 1.0
        print(stockName, " - High @9:45= ", highAt930)
        print(stockName, " - Low @9:45= ", lowAt930)
        lErr = ""

    return lErr, highAt930, lowAt930, diff930


def CheckForTrades(sessionId, stockName, lWb, high930, low930, diff930, slDiff, plDiff):

    lData, lErr = GetCandleData(sessionId, stockName, None, '09:45:00', '1')
    # lData, lErr = GetCandleData(sessionId, stockName, "2021-10-04", '09:45:00', '1')
    if lErr != None:
        print(lErr)
        sys.exit(1)

    df = pd.DataFrame(lData['intradayCandleData'])
    df = df.set_index(pd.DatetimeIndex(df['dateTime']))
    df['low'] = pd.to_numeric(df['low'])
    df['high'] = pd.to_numeric(df['high'])
    # print(df)

    return GoForTrade(sessionId, stockName, lWb, df, high930, low930, diff930, slDiff, plDiff)


def GoForTrade(sessionId, stockName, lWb, df, high930, low930, diff930, slDiff, plDiff):

    lNumOfShare = 100
    lBought = False
    lBoughtPrice = 0
    lOrigBoughtPrice = 0
    lBoughtPrint = False
    lJustBought = False
    lTSellCount = 0
    lBuyCount = 0

    lSold = False
    lSoldPrint = False

    lSlValue = low930 - 1
    # TSL :Trail Stop Loss, SELL: Sell on reaching Target
    lTslPrint= False
    lSlHitPrint = False
    lLossAbovePrint = False
    lLossPrint = False

    lTargetAction = "TSL"
    lRepeatBuys = True
    lBoughtFirst = False
    lForceSell = False

    lIsTradePossible = False
    lFTSellPrint = False
    lFTDOne = False

    lTarget=0
    lOkLossUpto = 500
    lOkDiff = 5
    lLocProfit = 0
    lGainBy1000 = 1000
    lGainBy1000Div = 2.0

    lStoxHigh = 0
    lStoxLow = 0

    print("\n\n" + stockName)

    # if diff930 < lOkDiff:
    #     lTxt = '\t' + bcolors.BOLD + bcolors.OKRED + f'**** DIFFERECE IS LESS:{slDiff}, NO TRADE POSSIBLE TODAY **** '
    #     lTxt = lTxt + bcolors.ENDC
    #     print(lTxt)
    #     lTxt = ""
    #     return plDiff


    for i in range(len(df['high'])):

        if lFTDOne:
            break

        if lBoughtFirst and lSold and (not lRepeatBuys):
            break

        lLTPH = df['high'][i]
        lLTPL = df['low'][i]
        lTxt = df["dateTime"][i] + " - " + str(df['high'][i]) + " - " + str(df['low'][i])

        if lLTPH > high930 and not lBought:
            lBought = True
            lBoughtPrice = lLTPH
            lOrigBoughtPrice = lLTPH
            lIsTradePossible = True
            lBoughtFirst = True
            lBuyCount += 1
            lStoxHigh = lLTPH
            lStoxLow = lLTPL

            lSlValue = low930 - 1

            if (lLTPH - low930) > 50:
                lSlValue = low930 + (lLTPH - low930)/2.0

            if lBuyCount >= 2:
                lSlValue = low930 + (lLTPL - low930)/2.0

            # if diff930 >= 10:
            #     lSlValue = lSlValue + diff930/2.0

            lTxt = lTxt + "\t\t" + bcolors.BOLD
            lTxt = lTxt + "BUY - " + "H/L: " + str(high930) + "/" + str(low930)
            lTxt = lTxt + " - BP: " + str(lLTPH)
            lTxt = lTxt + " - HLD: " + str(diff930)
            lTxt = lTxt + " - BHLD: " + str(lLTPH - low930)
            lTxt = lTxt + " - SL: " + str(lSlValue)
            lTxt = lTxt + bcolors.ENDC
            print(lTxt)
            continue

        if lBought:
            if lStoxHigh < lLTPH:
                lStoxHigh = lLTPH

            if lStoxLow > lLTPL:
                lStoxLow = lLTPL


        if lBought and (lLTPH - lBoughtPrice) >= slDiff:
            lTarget += 1
            # lDiffStopLoss = diff930

            if lTargetAction == "SELL":
                lSold = True
                lBought = False
                lTxt = lTxt + '\t\t' + bcolors.BOLD + bcolors.OKGREEN + 'SELL '
                lTxt = lTxt + " - SP: " + str(lLTPH)
                lTxt = lTxt + " - DIA: " + str(lLTPH - lOrigBoughtPrice)
                lTxt = lTxt + " - GAIN: " + str(lNumOfShare * (lLTPH - lOrigBoughtPrice))
                lTxt = lTxt + bcolors.ENDC
                print(lTxt)
                plDiff = plDiff + (lNumOfShare * (lLTPH - lOrigBoughtPrice))
                lLocProfit = lLocProfit + (lNumOfShare * (lLTPH - lOrigBoughtPrice))
                continue

            if lTargetAction == "TSL":
                lTSellCount += 1
                # lTarget += 1
                # Will implement SetTsl()
                # lSlValue = lLTPH - (lLTPH - lBoughtPrice) * 0.50
                lSlValue = lBoughtPrice

                if lTSellCount == 1:
                    lSlValue = 1 + lLTPH - (lLTPH - lBoughtPrice) / 2.0
                    # lSlValue = lLTPH

                if lTSellCount >= 2:
                    # lSlValue = lBoughtPrice + (lLTPH - lBoughtPrice) / 2.0
                    lSlValue = lLTPH
                # diff930 = 2 * diff930

                lGain = lNumOfShare * (lLTPH - lOrigBoughtPrice)
                if lGain > 5000:
                    lSlValue = lLTPH


                lTxt = lTxt + '\t\t' + bcolors.BOLD + bcolors.OKGREEN + "TSELL"
                lTxt = lTxt + ' - TSL: ' + str(lSlValue)
                # lTxt = lTxt + " - Diff.Amm: " + str(lLTPH - lBoughtPrice)
                lTxt = lTxt + " - GAIN: " + str(lNumOfShare * (lLTPH - lOrigBoughtPrice))
                lTxt = lTxt + bcolors.ENDC
                print(lTxt)
                lBoughtPrice = lLTPH
                lStoxLow = lLTPL
                # plDiff = plDiff + (lNumOfShare * (lLTPH - lBoughtPrice))
                continue

        if lBought and (lLTPL < lSlValue):
            lSold = True
            lBought = False
            # lTarget += 1
            lColor = bcolors.OKGREEN

            if lLTPL < lBoughtPrice:
                lColor = bcolors.WARNING

            if lLTPL < lOrigBoughtPrice:
                lColor = bcolors.OKRED

            lTxt = lTxt + '\t\t' + bcolors.BOLD + lColor + 'TSLH: '
            lTxt = lTxt + " - (High: " + str(high930) + ", Low: " + str(low930) + ")"
            lTxt = lTxt + " - Diff.Amm: " + str(lSlValue - lOrigBoughtPrice)
            lTxt = lTxt + " - GAIN: " + str(lNumOfShare * (lSlValue - lOrigBoughtPrice))
            lTxt = lTxt + bcolors.ENDC
            print(lTxt)
            plDiff = plDiff + (lNumOfShare * (lSlValue - lOrigBoughtPrice))
            lLocProfit = lLocProfit + (lNumOfShare * (lSlValue - lOrigBoughtPrice))

            # if lLocProfit <= 0:
            #     lFTDOne = True

            continue


        if not lJustBought and lBought:
            lLocLoss = lNumOfShare * (lBoughtPrice - lLTPL)
            if lLTPL < lBoughtPrice and lLocLoss > lOkLossUpto:
                lLossAbovePrint = True


        if lBought and ("15:10:00" in df["dateTime"][i]):
            lSold = True
            lBought = False
            lFTDOne = True
            lDiffAmm = lLTPH - lOrigBoughtPrice
            lColor = bcolors.OKGREEN
            if lDiffAmm <= 0:
                lColor = bcolors.OKRED

            lTxt = lTxt + '   \t' + bcolors.BOLD + lColor + 'FSELL'
            lTxt = lTxt + " - H/L: " + str(high930) + "/" + str(low930)
            lTxt = lTxt + " - DIA: " + str(lDiffAmm)
            lTxt = lTxt + " - GAIN/LOSS: " + str(lNumOfShare * (lLTPH - lOrigBoughtPrice))
            lTxt = lTxt + bcolors.ENDC
            print(lTxt)
            plDiff = plDiff + (lNumOfShare * (lLTPH - lOrigBoughtPrice))
            lLocProfit = lLocProfit + (lNumOfShare * (lLTPH - lOrigBoughtPrice))

        if lLossAbovePrint and lLossPrint:
            lTxt = lTxt + '   \t' + bcolors.BOLD + bcolors.WARNING + "LOSS SELL"
            lTxt = lTxt + " (High: " + str(high930) + ", Low: " + str(low930) + ")"
            lTxt = lTxt + " - Diff.Amm: " + str(lBoughtPrice - lLTPL)
            lTxt = lTxt + " - Loss: " + str(lNumOfShare * (lBoughtPrice - lLTPL))
            lTxt = lTxt + bcolors.ENDC
            lLossAbovePrint= False
            print(lTxt)
            plDiff = plDiff + (lNumOfShare * (lLTPH - lBoughtPrice))
            lLocProfit = lLocProfit + (lNumOfShare * (lLTPH - lOrigBoughtPrice))

        if lBought and (lNumOfShare * (lLTPH - lBoughtPrice)) >= lGainBy1000:
            lSlValue = 1 + lLTPH - (lLTPH - lBoughtPrice) / lGainBy1000Div
            lGainBy1000Div += + 1.0
            lTxt = lTxt + '   \t' + bcolors.BOLD + bcolors.OKGREEN
            lTxt = lTxt + 'TSL: ' + str(lSlValue)
            lTxt = lTxt + " - GAIN: " + str(lNumOfShare * (lLTPH - lBoughtPrice))
            lTxt = lTxt + bcolors.ENDC
            print(lTxt)
            lGainBy1000 += 1000


        if lBought and lForceSell and i == (len(df['high']) - 1):
            lSold = True
            lBought = False
            lFTDOne = True
            lDiffAmm = lLTPH - lOrigBoughtPrice
            lColor = bcolors.OKGREEN
            if lDiffAmm <= 0:
                lColor = bcolors.OKRED

            lTxt = lTxt + '   \t' + bcolors.BOLD + lColor + 'FORCE-SELL'
            lTxt = lTxt + " - H/L: " + str(high930) + "/" + str(low930)
            lTxt = lTxt + " - DIA: " + str(lDiffAmm)
            lTxt = lTxt + " - GAIN/LOSS: " + str(lNumOfShare * (lLTPH - lOrigBoughtPrice))
            lTxt = lTxt + bcolors.ENDC
            print(lTxt)
            plDiff = plDiff + (lNumOfShare * (lLTPH - lOrigBoughtPrice))
            lLocProfit = lLocProfit + (lNumOfShare * (lLTPH - lOrigBoughtPrice))


        lJustBought = False


    if not lIsTradePossible:
        lTxt = '\t' + bcolors.BOLD + bcolors.OKRED + f'**** NO TRADE POSSIBLE TODAY FOR \'{stockName}\' **** '
        lTxt = lTxt + bcolors.ENDC
        print(lTxt)
    else:
        lColor = bcolors.OKGREEN
        if lLocProfit < 0:
            lColor = bcolors.OKRED
        elif lLocProfit == 0:
            lColor = bcolors.WARNING
        lTxt = bcolors.BOLD + lColor + f'{stockName}= {lLocProfit} '
        lTxt = lTxt + f"\nBought: {lOrigBoughtPrice}"
        lTxt = lTxt + f"\nHigh: {lStoxHigh}"
        lTxt = lTxt + f"\nLow: {lStoxLow}"
        lTxt = lTxt + f"\nSL: {lSlValue}"
        lTxt = lTxt + bcolors.ENDC
        print(lTxt)

    print("\n\n\n")

    return plDiff



def ProcessStox(dfStox, sessionId, lWb):
    # print( dfStox['Symbol'])
    plDiff = 0
    for stockName in dfStox['Symbol']:
        lJson, lErr = GetCandleData(sessionId, stockName,None, '09:00:00', '15', '09:45:00')
        # lJson, lErr = GetCandleData(sessionId, stockName,"2021-10-04", '09:00:00', '15', '09:45:00')

        if lErr != None:
            print(lErr)
            print("INFO: Pl check the log...continue with other stox")
            continue

        # print(lJson)
        lErr, high930, low930, diff930 = ProcessCandleDataFor930(sessionId, stockName, lJson, lWb)
        if lErr==None:
            print("Error: 9:30 candle is not available..")
            continue

        # if not (diff930 >= 5 or diff930 >= ( high930 / 100.0)):
        #     continue

        slDiff = diff930

        # if diff930 > 30:
        #     slDiff = diff930 / 2.0


        plDiff = CheckForTrades(sessionId, stockName, lWb, high930, low930, diff930, slDiff, plDiff)
        print("Profit/Loss:", plDiff)

