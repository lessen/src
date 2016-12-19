from ranges import *
from random import random as r
from random import seed
from eg import eg

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

@eg
def _div1(n=1000):
  "1D cluster. Noise. Should divide evenly."
  for zz in div([r() for _ in range(n)]):
    xx = zz["x"]
    print("start  %.4f stop %.4f n %s" % (xx.lo, xx.hi, xx.n))

@eg
def _div2(n=1000):
  "1D cluster. random**3: most nums below half are very similar"
  for zz in div([r()**3 for _ in range(n)]):
    xx = zz["x"]
    print("start  %.4f stop %.4f n %s" % (xx.lo, xx.hi, xx.n))

@eg
def _div3():
  "1D cluster. Small population."
  _div1(20)

def first(x): return x[0]
def second(x): return x[1]

@eg
def _sdiv(n=1000):
  "2D. Y does not change except at 33 and 66"
  def cut(x):
    more = lambda x:x + (0.1*r())
    if x < 0.33: return more(0.33)
    if x < 0.66: return more(0.66)
    return more(1)
  lst0 = [r() for _ in range(n)]
  lst = [[x, cut(x)] for x in lst0]
  for zz in sdiv(lst):
    xx = zz["x"]
    yy = zz["y"]
    print("start  %.4f stop %.4f n %s " % (xx.lo, xx.hi, xx.n),end="")
    print("xmedian %.4f ymedian %.4f" % (xx.median(), yy.median()))

@eg    
def _ediv(n=1000):
  "2D class only changes symbols at .33 and .5"
  def cut(x):
    if x < 0.33: return "a"
    if x < 0.5 : return "b"
    return "c"
  lst0 = [r()**2 for i in range(n)]
  lst = [[x, cut(x)] for x in lst0]  
  for zz in ediv(lst):
     xx = zz["x"]
     print("start  %.4f stop %.4f n %s" % (xx.lo, xx.hi, xx.n))

@eg
def _ddiv1(n=1000):
  "1D: cluster similiar things"
  data = dict(rx1 = [10*r()**3 for _ in range(n)],
              rx2 = [10*r()**0.33   for _ in range(n)],
              rx4 = [10*r()**3 for _ in range(n)],
              rx3 = [10*r()      for _ in range(n)])
  ddv0(data)

@eg
def _ddiv2(n=100):
  ddv0(dict(x1=[0.34, 0.49, 0.51, 0.6],
            x2=[6,  7,  8,  9]))
  
@eg
def _ddiv20():
  ddv0(dict(x1=[0.34, 0.49, 0.51, 0.6],
            x2=[0.6,  0.7,  0.8,  0.9],
            x3=[0.15, 0.25, 0.4,  0.35],
            x4=[0.6,  0.7,  0.8,  0.9],
            x5=[0.1,  0.2,  0.3,  0.4]))


    
def ddv0(data):
  q = lambda z:round(z,3)
  for zz in ddiv(data):
    xx = zz["x"]
    yy = zz["y"]
    print("start  %.4f stop %.4f n %.4f" % (xx.lo, xx.hi, xx.n),end=" ")
    print("median %.4f mode %.4f has %s" % (xx.median(), yy.median(), len(zz["has"])),end= " ")
    print("has %s" % [s[0].label for s in zz["has"]])

    
  
eg()
