import datetime
import sys
import xlwings as xw
import pandas as pd
import requests
import json
import time

headers = {
  'Accept': 'application/json',
  # 'x-session-token': '676c3adfc62e33321680c3a6be3470b0'
}

def getDate(fmt="", lNow=None):

    if lNow == None:
        lNow = datetime.datetime.now()

    lTxt = lNow.strftime("%d_%m_%Y_%H_%M_%S")

    if fmt == "dd-mm-yyyy":
        lTxt = lNow.strftime("%d-%m-%Y")
    elif fmt == "dd-mm-yy":
        lTxt = lNow.strftime("%d-%b-%y")
    elif fmt == "yyyy-mm-dd":
        lTxt = lNow.strftime("%Y-%m-%d")
    elif fmt == "dd-mmm-yyyy":
        lTxt = lNow.strftime("%d-%b-%Y")
    elif fmt == "dd-mon-yyyy":
        lTxt = lNow.strftime("%d-%b-%Y")
    elif fmt == "dd-month-yyyy":
        lTxt = lNow.strftime("%d-%B-%Y")
    elif fmt == "yyyy":
        lTxt = lNow.strftime("%Y")
    elif fmt == "yy":
        lTxt = lNow.strftime("%y")
    elif fmt == "month":
        lTxt = lNow.strftime("%B")
    elif fmt == "mmm":
        lTxt = lNow.strftime("%b")
    elif fmt == "mm":
        lTxt = lNow.strftime("%m")
    elif fmt == "dd":
        lTxt = lNow.strftime("%d")
    elif fmt == "hh-mm-ss":
        lTxt = lNow.strftime("%H-%M-%S")
    elif fmt == "hh:mm:ss":
        lTxt = lNow.strftime("%H:%M:%S")
    elif fmt == "hrs":
        lTxt = lNow.strftime("%H")
    elif fmt == "min":
        lTxt = lNow.strftime("%M")
    elif fmt == "sec":
        lTxt = lNow.strftime("%S")

    return lTxt

def PrintLine(str="=", rep=20):
    print(str*rep)

def PrintList(list, title="LIST/ARRAY/LINES"):

    lLen = len(title) + 10
    PrintLine(rep=lLen)
    print(" " * 5 + title)
    PrintLine(rep=lLen)

    cnt=0
    for i in list:
        cnt=cnt+1
        print(str(cnt) + ". " + i)

    PrintLine(rep=lLen)

def FileReadLines(fname, opt="r"):
    lErr=None
    lFileLines=None
    try:
        f = open(fname, opt)
        lFileLines = f.read().split("\n")
        f.close()
    except OSError as err:
        lErr="OS error: {0}".format(err)
    except:
        lErr = "unable to open file"

    return lFileLines, lErr

def FileRead(fname, opt="r"):
    lErr=None
    lFileLines=None
    try:
        f = open(fname, opt)
        lFileLines = f.read()
        f.close()
    except OSError as err:
        lErr="OS error: {0}".format(err)
    except:
        lErr = "unable to open file"

    return lFileLines, lErr

def getOsName():
    lOsName = sys.platform
    #print(lOsName)
    if lOsName.startswith('darwin'):
        lOs = 'darwin'
    elif lOsName.startswith('win'):
        lOs = 'windows'
    elif lOsName.startswith('linux'):
        lOs = 'linux'

    return lOs


def getPassword(passwd):
    translated = ''  # cipher text is stored in this variable
    i = len(passwd) - 1

    while i >= 0:
        translated = translated + passwd[i]
        i = i - 1
    return translated


def GetWorkbook(xlsfile):
    lWb=None
    lErr=None

    try:
        lWb = xw.Book(xlsfile)
    except Exception as err:
        lErr=f"\nError: File \'{xlsfile}\' is not found!"
        print(err)

    if lErr!=None:
        return lWb, lErr

    return lWb, lErr


def GetSessionId(lWb):
    lErr=None
    lSessionId=None

    sheetNames = [lWb.sheets(i).name for i in range(1, lWb.sheets.count + 1)]

    if 'Login' not in sheetNames:
        lErr="Error: Sheet 'Login' not found, cannot proceed!"

    if lErr!=None:
        return lSessionId, lErr

    sheetLogin = lWb.sheets("Login")
    lSessionId=str(sheetLogin.range('A4').value)

    return lSessionId, lErr



def GetLogin(xlsfile):
    lWb=None
    lErr=None
    lLoginList=None

    try:
        lWb = xw.Book(xlsfile)
    except Exception as err:
        lErr=f"\nError: File \'{xlsfile}\' is not found!"
        print(err)

    if lErr!=None:
        return lWb, lLoginList, lErr

    sheetNames = [lWb.sheets(i).name for i in range(1, lWb.sheets.count + 1)]

    if 'Login' not in sheetNames:
        lErr="Error: Sheet 'Login' not found, cannot proceed!"

    if lErr!=None:
        return lWb, lLoginList, lErr

    sheetLogin = lWb.sheets("Login")

    lLoginId= getPassword(sheetLogin.range('A1').value)
    lPasswd=getPassword(sheetLogin.range('A2').value)
    lYob=str(sheetLogin.range('A3').value)
    lSession=str(sheetLogin.range('A4').value)
    lLoginList=[lLoginId, lPasswd, lYob, lSession]

    return lWb, lLoginList, lErr


def GetStocksList(lWb):
    lErr=None
    lStoxList=None
    lDf=None

    sheetNames = [lWb.sheets(i).name for i in range(1, lWb.sheets.count + 1)]

    if 'Stox' not in sheetNames:
        lErr="Error: Sheet 'Stox' not found, cannot proceed!"

    if lErr!=None:
        return lStoxList, lErr

    lSheetStox = lWb.sheets("Stox")

    # print(lSheetStox.range("A1").expand().value)
    lDf = lSheetStox.range('A1').expand().options(pd.DataFrame).value
    lDf.reset_index(inplace=True)
    # print (lDf)
    return lDf, lErr



def DoSamcoLogin(lWb, lLoginList):
    lErr=None
    lSessionToken=None

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    requestBody = {
        "userId": lLoginList[0],
        "password": lLoginList[1],
        "yob": lLoginList[2]
    }

    try:
        lRes = requests.post('https://api.stocknote.com/login', data=json.dumps(requestBody), headers=headers)
        lJson= lRes.json()
        lStatus = lJson['status']

        if lStatus == "Success":
            lSessionToken = lJson['sessionToken']
            # print("Session: " + lSessionToken)
            sheetLogin = lWb.sheets("Login")
            sheetLogin.range('A4').value = lSessionToken
        else:
            lErr=f"Error: login not success.\n{lRes}"
    except Exception as err:
        lErr=f"Error:{err}."
        # print(lErr)

    return lSessionToken, lErr

def DoSamcoGetLimits(lLoginList):
    headers['x-session-token'] = lLoginList[3]
    lJson=None
    lErr=None

    try:
        lRes = requests.get('https://api.stocknote.com/limit/getLimits', headers=headers)
        lJson = lRes.json()
        lStatus = lJson['status']

        if lStatus != "Success":
            lErr = f"Error: login not success.\n{lJson['statusMessage']}"
    except Exception as err:
        lErr = f"Error: {err}."


    return lJson, lErr


def IsSamcoSessionExpired(lLoginList):
    headers['x-session-token'] = lLoginList[3]
    lErr = None

    try:
        lRes = requests.get('https://api.stocknote.com/limit/getLimits', headers=headers)
        lJson = lRes.json()
        lStatus = lJson['status']
        lStatusMsg = lJson['statusMessage']

        if lStatus != "Success":
            lErr=f"Error: {lStatusMsg}"

    except Exception as err:
        lErr = f"Error: {err}."

    return lErr

def GetIntradaySym(xlsfile):
    lWb=None
    lErr=None
    lLoginList=None

    try:
        lWb = xw.Book(xlsfile)
    except Exception as err:
        lErr=f"\nError: File \'{xlsfile}\' is not found!"
        print(err)

    if lErr!=None:
        return lWb, lLoginList, lErr

    sheetNames = [lWb.sheets(i).name for i in range(1, lWb.sheets.count + 1)]

    if 'Intraday' not in sheetNames:
        lErr="Error: Sheet 'Intraday' not found, cannot proceed!"

    if lErr!=None:
        return lWb, lLoginList, lErr

    sheetLogin = lWb.sheets("Intraday")

    lSymName= sheetLogin.range('A1').value

    if lSymName == "":
        lErr = "Error: No Symbol Name found."

    return lSymName, lErr


def GetHistoryCandleData(pSessionId, pSymName, pDateFor=None, pTimeFrom='09:00:00', pInterval='15', pTimeTo=None):

    lDate = pDateFor
    lErr = None
    lJson = None

    if pDateFor == None:
        lDate = getDate(fmt="yyyy-mm-dd")

    paramsDict = {
        'symbolName': pSymName,
        'fromDate': lDate + ' ' + pTimeFrom,
        'interval': pInterval
    }

    if pTimeTo != None:
        paramsDict['toDate'] = lDate + ' ' + pTimeTo

    headers['x-session-token'] = pSessionId

    try:
        lRes = requests.get('https://api.stocknote.com/history/candleData', params= paramsDict, headers=headers)
        lJson = lRes.json()
        lStatus = lJson['status']

        if lStatus != "Success":
            lErr = f"Error: not success.\n{lJson['statusMessage']}"

    except Exception as err:
        lErr = f"Error: {err}."

    return lJson, lErr



def GetCandleData(pSessionId, pSymName, pDateFor=None, pTimeFrom='09:00:00', pInterval='15', pTimeTo=None):

    lDate = pDateFor
    lErr = None
    lJson = None

    if pDateFor == None:
        lDate = getDate(fmt="yyyy-mm-dd")

    paramsDict = {
        'symbolName': pSymName,
        'fromDate': lDate + ' ' + pTimeFrom,
        'interval': pInterval
    }

    if pTimeTo != None:
        paramsDict['toDate'] = lDate + ' ' + pTimeTo

    headers['x-session-token'] = pSessionId

    try:
        lRes = requests.get('https://api.stocknote.com/intraday/candleData', params= paramsDict, headers=headers)
        lJson = lRes.json()
        lStatus = lJson['status']

        if lStatus != "Success":
            lErr = f"Error: not success.\n{lJson['statusMessage']}"

    except Exception as err:
        lErr = f"Error: {err}."

    return lJson, lErr


def GetQuote(lLoginList, pSymName):

    lErr = None
    lJson = None
    paramsDict = {
        'symbolName': pSymName
    }
    headers['x-session-token'] = lLoginList[3]

    try:
        lRes = requests.get('https://api.stocknote.com/quote/getQuote', params=paramsDict, headers=headers)
        lJson = lRes.json()
        lStatus = lJson['status']

        if lStatus != "Success":
            lErr = f"Error: not success.\n{lJson['statusMessage']}"

    except Exception as err:
        lErr = f"Error: {err}."

    return lJson, lErr

def GetIndex():
    lDictMap = {}
    lStox = []
    lJson = None
    lErr = None

    lNseHeader = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.206"
    }

    lOkOk = True
    while lOkOk:
        lRes = requests.get("https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050", headers=lNseHeader)

        if lRes.status_code == 200:
            lOkOk = False
            lJson = lRes.json()
            for i in range(len(lJson['data'])):
                lDictMap[lJson['data'][i]['symbol']] = lJson['data'][i]['pChange']
                lStox.append(lJson['data'][i]['symbol'])
              # print(lJson['data'][i]['symbol'],":",lJson['data'][i]['pChange'] )
        else:
            time.sleep(3)

    return lErr, lStox, lDictMap, lJson
