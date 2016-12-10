from ranges1 import num,sym,ranges
from random import random as r
from random import seed

def _symnum():
  seed(1)
  lst=[10,11,12,13,14,15,16,17,18,19,20,
       21,22,23,24,25,26,27,28,29,30,31,32,33,34]
  x = num(lst)
  assert round(x.mu,3)==22.000
  assert round(x.sd,3)==7.360
  assert x.median() == 22
  assert x.lo == 10
  assert x.hi == 34
  y = sym(["a"]*9)
  for z in ["b"]*5: y + z
  assert round(y.ent(),3) == 0.940
  z = num([1,2])
  assert z.median() == 1.5
  z = num([1,2,3,4])
  assert z.median() == 2.5
 
def _ranges():
  for x in ranges([r() for _ in range(1000)]):
    pass #print(x)
  
for f in [_symnum,_ranges]:
  try: f()
  except Exception as e: print("E> bad",f.__name__,":",e)
  
_ranges()

