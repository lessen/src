import zipfile,re

def csv(str=None, file=None, zip=None,
         seperator= ",",
         missing  = "?",
         header   = True,
         white    = '([\n\r\t]|#.*)'): 
 # ------------------------------
 def same(x) : return x
 def utf8(x) : return x.decode("utf-8")
 def compile(lst,rules):
   def isa(x):
     try:  int(x); return int
     except ValueError:
       try:  float(x); return float
       except ValueError:
         return same
   def comp1(i,x):
     if x != missing:
       rule = rules[i] = rules[i] or isa(x)
       return rule(x)
     return x
   return [comp1(i,cell) for i,cell in enumerate(lst)]
 # ------------------------------         
 def worker(src,n=0,rules=[], lines=[], filter=same):
   for line0 in src:
     line1 = filter(line0)
     line2 = re.sub(white, "", line1)
     if line2:
       lines += [line2]
       if line2[-1] != seperator:
         tmp   = ''.join(lines)
         lines = []
         row   = [z.strip() for z in tmp.split(",")]
         if len(row)> 0:
           n += 1
           if n==1:
             rules = [None] * len(row)
           yield row if n==1 and header else compile(row,rules)
 # -----------------------      
 if zip:
   with zipfile.ZipFile(zip, 'r') as myzip:
     with myzip.open(file) as src:
       for row in worker(src,filter=utf8):
         yield row
 elif file:
   with open(file) as src:
     for row in worker(src):
       yield row  
 elif str:
   for row in worker(str.splitlines()):
     yield row

if __name__ == "__main__":
  import time,os
  stringOfData="""a,b,
  c,d
  1,2.0,3,x
  10,20,30,y"""
  for row in csv(stringOfData, header=True):
    print(row)
  if os.path.isfile("data/weather.csv") and \
     os.path.isfile("data/weatherLarge.csv") and\
     os.path.isfile("data/data.zip"):
    for row in csv(file="data/weather.csv"):
      print(row)
    m,t1=1,time.time()
    for row2 in csv(file="data/weatherLarge.csv"):
      m += 1
    n,t2=1,time.time()
    for row1 in csv(file="weatherLarge.csv",
                    zip="data/data.zip"):
      n += 1
    t3=time.time()
    print(m,t2-t1,row1) # reading from raw ascii
    print(n,t3-t2,row2) # reading from zip is slightly faster 
  
