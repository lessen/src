
# csveg

import time,os
from csv import csv
from eg  import eg

@eg
def _csvFromString():
   "demo of read from string..."
   stringOfData="""a,b,
   c,d
   1,2.0,3,x
   10,20,30,y"""
   for row in csv(stringOfData, header=True):
      print(row)
   print(row)
   assert row == [10, 20.0, 30, 'y']

@eg
def _csvFromSimpleFile():
  "Reading a few Ascii rows."
  for row in csv(file="data/weather.csv"):
    print(row)
  
  assert row == ['rainy', 71.0, 'TRUE', 'no']

@eg
def _csvFromLargeFile(n=0):
    "Reading over 50MB+ of data."
    print("\nPlz wait a few seconds while I read 100MB+ of data...")
    for row in csv(file="data/weatherLarge.csv"):
      n +=1
    print(n,row)
    assert row == ['rainy', 71.0, 'TRUE', 'no']
    assert n == 1835009

@eg
def _csvFromZip(n=0):
    "Reading over 50MB of data."
    for row in csv(file="weatherLarge.csv",
                      zip="data/data.zip"):
      n += 1
      
    assert row == ['rainy', 71.0,  91,'TRUE', 'no']
    assert n == 1835009
    
if __name__ == "__main__": eg()
```

