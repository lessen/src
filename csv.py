# -8_ python -*-
# CSV reader
# Copyright (c) 2016 Tim Menzies, 
#
# Usage:
#
#    for row in csv(...):
#       doSoemthing(row)
#
#  1. Can read from strings, files, zip files.
#  2. Rows divided on a seperator (usually ",").
#  3. Rows ending with "," are joined to the next row.
#  4. Row comments and whitespace are pruned.
#  5. Cells marked as `missing` are ignored.
#  6. Columns of ints and floats are coerced
#     to their propery type.
#  7. If `header=True` then the first line is
#     returned verbatim.
#  8. Column types are inferred from the first
#     non-header non-missing item in each column.
#  9. Column types are inferred and cached
#     (this speeds up load time ten-fold).
# 10. Zero dependancies on other Timm Tool code.
#
# For code that implements all the above, see
# (e.g.) `#1` for code that handles (e.g.) 1. in the source code.

import zipfile,re


def csv(str=None, file=None, zip=None, #.. 1
         seperator= ",",               #.. 2
         missing  = "?",               #.. 5
         header   = True,              #.. 7
         white    = '([\n\r\t]|#.*)'): #.. 4
 # ------------------------------
 def same(x) : return x
 def utf8(x) : return x.decode("utf-8")
 def compile(lst,rules):
   def isa(x):       #.................. 6
     try:  int(x); return int
     except ValueError:
       try:  float(x); return float
       except ValueError:
         return same
   def comp1(i,x):
     if x != missing:
       rule = rules[i] = rules[i] or isa(x) #.. 6,8,9
       return rule(x)
     return x
   return [comp1(i,cell) for i,cell in enumerate(lst)]
 # ------------------------------         
 def worker(src,n=0,rules=[], lines=[], filter=same):
   for line0 in src:
     line1 = filter(line0)
     line2 = re.sub(white, "", line1)  #............................ 4
     if line2:
       lines += [line2]
       if line2[-1] != seperator: #................................. 3
         tmp   = ''.join(lines)   #................................. 3
         lines = []
         row   = [z.strip() for z in tmp.split(",")] #.............. 4
         if len(row)> 0:
           n += 1
           if n==1:
             rules = [None] * len(row) #............................ 9
           yield row if n==1 and header else compile(row,rules) #... 7
 # -----------------------      
 if zip:
   with zipfile.ZipFile(zip, 'r') as myzip: #....... 1
     with myzip.open(file) as src:
       for row in worker(src,filter=utf8):
         yield row
 elif file:
   with open(file) as src: #........................ 1
     for row in worker(src):
       yield row  
 elif str:
   for row in worker(str.splitlines()): #........... 1
     yield row

###########################
# Demo code

if __name__ == "__main__":
  import time,os
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
    m,t1=1,time.time()
    print("\nPlz wait 10 seconds while I read 100MB+ of data...")
    print("Demo of reading from file...")
    for row1 in csv(file="data/weatherLarge.csv"):
      m += 1
    n,t2=1,time.time()
    print("... more reading of big files ...\n")
    print("Demo of reading from zip...")
    for row2 in csv(file="weatherLarge.csv",
                    zip="data/data.zip"):
      n += 1
    t3=time.time()
    print(m,t2-t1,row1) # reading from raw ascii
    print(n,t3-t2,row2) # reading from zip is slightly faster 
  
