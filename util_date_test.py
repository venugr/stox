from  util import *

print(getDate())
print(getDate("dd-mmm-yyyy"))
print(getDate("dd-month-yyyy"))
print ( "-"*10)
print(getDate("yyyy"))
print(getDate("yy"))
print ( "-"*10)
print(getDate("month"))
print(getDate("mmm"))
print(getDate("mm"))
print ( "-"*10)
print(getDate("dd"))

print ( "="*40)
dateval = "22/11/1972"
date_val = datetime.datetime.strptime(dateval, "%d/%m/%Y")
print(getDate("dd-month-yyyy", date_val))
print(getDate("dd-mon-yyyy", date_val))
print(getDate("dd-mm-yyyy", date_val))
print ( "-"*10)
print(getDate("month", date_val))
print(getDate("mmm", date_val))
print(getDate("mm", date_val))
print ( "="*40)
print(getDate("hh-mm-ss"))
print(getDate("hh:mm:ss"))
print ( "-"*10)
print(getDate("hrs"))
print(getDate("min"))
print(getDate("sec"))






