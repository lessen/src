from ranges1 import *
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
 
def _ranges1():
  for x in ranges([r()**2 for _ in range(10000)],
                  verbose=True):
    for k in ["start","stop","n"]:
      print(k, "%5s" %round(x[k],3),end=" ")
    print("")

def first(x): return x[0]
def second(x): return x[1]


def _ranges2():
  n=1000
  def cut(x):
    more = lambda x:x - (0.2+2*0.2*r())
    if x < 0.6: return more(0.3)
    if x < 0.85: return more(0.7)
    return more(1)
  lst0 = [r()**2 for _ in range(n)]
  lst = [[x, cut(x)] for x in lst0]
  print(">>",lst[-1])
  for x in ranges(lst,
                  key=first,
                  x=first,
                  y=second,
                  verbose=True):
    for k in ["start","stop","n"]:
      print(k, "%5s" %round(x[k],3),end=" ")
    print("")

def _ranges3():
  n=1000
  def cut(x):
    if x < 0.6: return "a"
    return "c"
 #   if x < 0.85: return "b"
  #  return "c"
  lst0 = [r()**2 for _ in range(n)]
  lst = [[x, cut(x)] for x in lst0]
  print(">>",lst[-1])
  for x in ranges(lst,
                  key=first,
                  x=first,
                  y=second,
                  ynum=False,
                  verbose=True):
    for k in ["start","stop","n"]:
      print(k, "%5s" %round(x[k],3),end=" ")
    print("")

seed(1)
  
_ranges1()
print("------------")
_ranges2()
print("-------")
_ranges3()

