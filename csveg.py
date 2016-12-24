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

@eg
def _csvFromSimpleFile():
  for row in csv(file="data/weather.csv"):
    print(row)

@eg
def _csvFromLargeFile(m=0):
    print("\nPlz wait 10 seconds while I read 100MB+ of data...")
    for row1 in csv(file="data/weatherLarge.csv"):
      m += 1
    print(m)

@eg
def _csvFromZip(n=0):
    for row2 in csv(file="weatherLarge.csv",
                      zip="data/data.zip"):
      n += 1
    print(n)

if __name__ == "__main__": eg()
