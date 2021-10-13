import sys
import pandas as pd

from  util import *

pd.set_option('display.width', 1500)
pd.set_option('display.max_rows', 150)
pd.set_option('display.max_columns', 50)

lines, err =FileReadLines("util.py")
if err != None:
    print(err)
else:
    print(type(lines))
    #PrintList(lines, "File: util.py, Contents/Lines.............")

PrintLine()

lines, err =FileRead("util_file_test.py")
if err != None:
    print(err)
else:
    print(type(lines))
    #print(lines)

print( "OS Name: " + getOsName())
#
# pwdText= getPassword("u!get!it!123")
# print(pwdText)
# print(getPassword(pwdText))
#
# pwdText= getPassword("RV32577")
# print(pwdText)

lWb,lLoginList, lErr=GetLogin('/Users/venul/PycharmProjects/pythonProject1/venv/AutoTrade/samco.xlsx')

if lErr != None:
    print(lErr)
    sys.exit(1)

# print(lLoginList)

if lLoginList[3] == "":
    DoSamcoLogin(lWb, lLoginList)

# lErr=IsSamcoSessionExpired(lLoginList)
# if lErr != None:
#     print(lErr)

# lData, lErr = DoSamcoGetLimits(lLoginList)
# if lErr != None:
#     print(lErr)
#     sys.exit(1)
# print(lData)
# lGrsMargin=lData['equityLimit']['grossAvailableMargin']
# lNetMargin=lData['equityLimit']['netAvailableMargin']
# print(lGrsMargin, lNetMargin)

# pd.set_option('display.width', 1500)
# pd.set_option('display.max_rows', 150)
# pd.set_option('display.max_columns', 50)
# df = pd.DataFrame(lData)
# print(df)



lSymName, lErr = GetIntradaySym('/Users/venul/PycharmProjects/pythonProject1/venv/AutoTrade/samco.xlsx')
if lErr != None:
    print(lErr)
    sys.exit(1)

print(lSymName)

lData, lErr = GetCandleData(lLoginList, lSymName)

if lErr != None:
    print(lErr)
    sys.exit(1)
# print(lData)

df = pd.DataFrame(lData['intradayCandleData'])
df = df.set_index(pd.DatetimeIndex(df['dateTime']))
df['low'] = pd.to_numeric(df['low'])
df['high'] = pd.to_numeric(df['high'])
print(df)
# print(type(df['low'][2]))
highAt930=df['high'][2]
lowAt930=df['low'][2]

print("High @9:45= ", highAt930)
print("Low @9:45= ", lowAt930)
#print(df.head())
dfDesc = df.describe()
print(dfDesc)
print( type(dfDesc))
print( type(df))
print(dfDesc['high']['min'])

