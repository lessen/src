from ranges import *
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
 
def _div(n=1000):
  for zz in div([r()**2 for _ in range(n)]):
    xx = zz["x"]
    print("start  %.4f stop %.4f n %s" % (xx.lo, xx.hi, xx.n))

def first(x): return x[0]
def second(x): return x[1]


def _sdiv(n=1000):
  def cut(x):
    more = lambda x:x - (0.2+2*0.2*r())
    if x < 0.6: return more(0.3)
    if x < 0.85: return more(0.7)
    return more(1)
  lst0 = [r()**2 for _ in range(n)]
  lst = [[x, cut(x)] for x in lst0]
  for zz in sdiv(lst):
    xx = zz["x"]
    print("start  %.4f stop %.4f n %s" % (xx.lo, xx.hi, xx.n))
    
def _ediv(n=1000):
  def cut(x):
    return "a" if x < 0.65 else "b"
  lst0 = [r()**2 for i in range(n)]
  lst = [[x, cut(x)] for x in lst0]  
  for zz in ediv(lst):
     xx = zz["x"]
     print("start  %.4f stop %.4f n %s" % (xx.lo, xx.hi, xx.n))
    
def _ddiv(n=1000):
  data = dict(rx1 = [10*r()**3 for _ in range(n)],
              rx2 = [10*r()**0.33   for _ in range(n)],
              rx3 = [10*r()      for _ in range(n)])
  q = lambda z:round(z,3)
  for z in ddiv(data):
    xx = z["x"]
    yy = z["y"]
    print("start  %.4f stop %.4f n %.4f" % (xx.lo, xx.hi, xx.n),end=" ")
    print("median %.4f mode %.4f "      % (xx.median(), yy.median()))
    
seed(1)
  
for f in [_div,_sdiv,_ediv,_ddiv]:
#for f in [_ddiv]:
  n=1000
  print("\n# ------------\n#",f.__name__)
  f(n)

