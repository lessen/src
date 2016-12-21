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
           else:
             assert len(row) == len(rules),("expected %s cells in this row" % len(rules))
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
