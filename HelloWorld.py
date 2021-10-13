import json

# print ("Hello, World")

import datetime
import dateutil
import requests

# print ( datetime.datetime.now())
# print ( datetime.datetime.now().strftime("%Y/%m/%d"))
#
# dateval = "22/11/1972"
# date_val = datetime.datetime.strptime(dateval, "%d/%m/%Y")
# print(date_val)
#
# noofdays = datetime.datetime.now() - date_val
#
# print( noofdays)
#
# birthdate = datetime.datetime.now() - datetime.timedelta(days=17808)
# print ( birthdate)
#
# birthdate = datetime.datetime.now() - datetime.timedelta(days=noofdays.days)
# print ( birthdate.strftime("%d-%b-%Y"))
# print ( birthdate.strftime("%d-%B-%Y"))

# -----------------------

# f = open("testing.txt", "r")
# print(f.read())
# f.close()
#
# with open("testing.txt", "r") as line:
#     print(line.read())
#
#
# custom_header = {
#     'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.206"}

# r = requests.get("https://www1.nseindia.com/live_market/dynaContent/live_watch/stock_watch/niftyStockWatch.json", headers=custom_header)
# print ( type(r.text) )
#
# data = json.loads(r.text)
# print(type(data))
# print(data)
#
# print(data['declines'])
#
# nicedata = json.dumps( data, indent=3, sort_keys= True)
#
# print( nicedata)
#
# with open("nifity.data", "w") as line:
#     line.write(nicedata)
################################################
custom_header = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.206"}


import pandas as pd
# df = pd.DataFrame([(11,111),(22,222),(33,333)],['a','b','c'],['AA','BB'])
# print(df)
#
# dict_val = {"Wipro": {'open': 500, 'high':575, 'close': 515}, "Infy": {'open':700, 'high':700, 'close': 687}}
# df = pd.DataFrame().from_dict(dict_val)
# print(df)
# print(df.transpose())

r = requests.get("https://www1.nseindia.com/live_market/dynaContent/live_watch/stock_watch/niftyStockWatch.json", headers=custom_header).json()
# print(r['data'])

pd.set_option('display.width', 1500)
pd.set_option('display.max_rows', 150)
pd.set_option('display.max_columns', 50)
df = pd.DataFrame(r['data'])
# print(list(df))
df = df[['symbol', 'open','high','low', 'ltP']]
# print(df)
# print(list(df))

print(df.head(5))
print(df.tail(5))
print(df['low'].tail(5))
print(df['low'].iloc[45])
print(df['low'].iloc[-1])
print(df['low'].iloc[-0])

print("*"*50)
print(df.loc[0])
print(df.loc[0]['symbol'])
print(df.loc[0].at['high'])

print("*"*50)
df.set_index('symbol', inplace=True)
print(df)
print(df.loc['IOC'].at['open'])

def conver_rupee(val):
    newVal = val.replace(",","")
    return float(newVal)

df['ltP'] = df['ltP'].apply(conver_rupee)
df1 = df[df['ltP'] > 10000]
print(df1)

df1 = df[(df['ltP'] > 1000) & (df['ltP'] < 3000)]
print(df1)

df1 = df[(df['ltP'] > 2000) & (df['ltP'] < 3000)]
print(df1)


print(df.loc['IOC':'WIPRO'])








