import time,os
from csv import csv
from eg  import eg


print("Demo of read from string...")

stringOfData="""a,b,
c,d
1,2.0,3,x
10,20,30,y"""

for row in csv(stringOfData, header=True):
  print(row)

  if os.path.isfile("data/weather.csv") and \
   os.path.isfile("data/weatherLarge.csv") and\
   os.path.isfile("data/data.zip"):
  print("\nDemo of read from file...")
  for row in csv(file="data/weather.csv"):
    print(row)
  m,t1=1,time.process_time()
  print("\nPlz wait 10 seconds while I read 100MB+ of data...")
  print("Demo of reading from file...")
  for row1 in csv(file="data/weatherLarge.csv"):
    m += 1
  n,t2=1,time.process_time()
  print("... more reading of big files ...\n")
  print("Demo of reading from zip...")
  for row2 in csv(file="weatherLarge.csv",
                    zip="data/data.zip"):
    n += 1
  t3=time.process_time()
  print(m,t2-t1,row1) # reading from raw ascii
  print(n,t3-t2,row2) # reading from zip is slightly faster 
  
