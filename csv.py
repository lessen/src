import zipfile,re

def csv(str=None, file=None, zip=None,
         seperator= ",",
         missing  = "?",
         header   = True,
         white    = '([\n\r\t]|#.*)'): 
 # ------------------------------
 def same(x,*_): return x
 def compiler(lst,rules):
   def atom(z):
     try:  return int(z),int
     except ValueError:
       try:  return float(z),float
       except ValueError:
         return z, same   
   # ---------------
   def compile(i,x):
     if x != missing:
       if rules[i] is None:
         x,rule   = atom(x)
         rules[i] = rule
       return rules[i](x)
     return x
   # ---------------
   return [compile(i,cell) for i,cell in enumerate(lst)]
 # ------------------------------         
 def worker(src):
   cache = []
   rules = []
   prep  = same if header else compiler
   for line in src:
     line = re.sub(white, "", line)
     if line:
       cache += [line]
       if line[-1] != seperator:
         line  = ''.join(cache)
         cache = []
         row  = [z.strip() for z in line.split(",")]
         if len(row)> 0:
           if not rules:
             rules = [None] * len(row)
           yield prep(row,rules)
           prep = compiler
 # -----------------------      
 if zip:
   with zipfile.ZipFile(zip, 'r') as myzip:
     with myzip.open(file, mode='r') as src:
       for row in worker(src):
         yield src
 elif file:
   with open(file) as src:
     for row in worker(src):
       yield row  
 elif str:
   for row in worker(str.splitlines()):
     yield row

if __name__ == "__main__":
  data="""a,b,
  c,d
  1,2,3,x
  10,20,30,y"""
  for row in csv(data,header=True):
    print(row)
  for row in csv(file="data/weather.csv"):
    print(row)
  for row in csv(file="weather.csv",
                 zip="data/data.zip"):
    print(row)


