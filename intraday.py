import sys
import pandas as pd
import time
from util import *
from intraday_stox import *

pd.set_option('display.width', 1500)
pd.set_option('display.max_rows', 1500)
pd.set_option('display.max_columns', 50)

class stoxData:
    symbol: None
    highAt930: None
    lowAt930: None
    diff930: None






def startIntraday():

    lXlxFile = '/Users/venul/PycharmProjects/pythonProject1/venv/AutoTrade/samco.xlsx'
    lWb, lErr = GetWorkbook(lXlxFile)
    if lErr != None:
        print(lErr)
        sys.exit(1)


    sessionId, lErr = GetSessionId(lWb)
    if lErr != None:
        print(lErr)
        sys.exit(1)

    if sessionId == None:
        print("Error: something went wrong.")
        sys.exit(1)

    dfStox, lErr = GetStocksList(lWb)
    if lErr != None:
        print(lErr)
        sys.exit(1)

    lErr, lStox, lDictStox, lJson = GetIndex()
    if lErr != None:
        print(lErr)
        sys.exit(1)

    print(lStox)
    for i in range(1, 11):
        print(lStox[i])
    # print(lJson)
    # sys.exit(1)

    for i in range(1, 11):
        print(lStox[i], ":", lDictStox[lStox[i]])

    ProcessStox(dfStox, sessionId, lWb)
    # ProcessStox(lStox[1:6], sessionId, lWb)



if __name__ == '__main__':
    while True:
        try:
            startIntraday()
        except Exception:
            print("Proceeding...")
        print("waiting for next fetch...")
        time.sleep(60*1)
        print("*" * 60)