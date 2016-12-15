import zipfile,re

def csv(str=None, file=None, zip=None,
         seperator= ",",
         missing  = "?",
         header   = True,
         white    = '([\n\r\t]|#.*)'): 
 # ------------------------------
 def same(x,*_): return x
 def utf8(x)   : return x.decode("utf-8")
 def compile(lst,rules):
   def atom(z):
     try:  return int(z),int
     except ValueError:
       try:  return float(z),float
       except ValueError:
         return z, same
   def comp1(i,x):
     if x != missing:
       if rules[i] is None:
         x,rule   = atom(x)
         rules[i] = rule
       return rules[i](x)
     return x
   return [comp1(i,cell) for i,cell in enumerate(lst)]
 # ------------------------------         
 def worker(src,n=0,rules=[], lines=[],filter=same):
   for line0 in src:
     line1 = filter(line0)
     line2 = re.sub(white, "", line1)
     print("line",line2)
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
         yield src
 elif file:
   with open(file) as src:
     for row in worker(src):
       yield row  
 elif str:
   for row in worker(str.splitlines()):
     yield row

if __name__ == "__main__":
  import time
  data="""a,b,
  c,d
  1,2,3,x
  10,20,30,y"""
  for row in csv(data,header=True):
    print(row)
  for row in csv(file="data/weather.csv"):
    print(row)
  with zipfile.ZipFile("data/data.zip") as z:
    with z.open("weather.csv") as f:
      for row in f:
        print(row) #.encode('utf-8'))
  for row in csv(file="weather.csv",zip="data/data.zip"):
    print(1,row)
#  t1 = time.time()
#  n=1
#  for row in csv(file="data/weatherLarge.csv"): n+= 1
#  t2 = time.time()
#  print(n,t2-t1,row)

