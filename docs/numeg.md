
# numeg

from num import num
from eg import eg
from random import random as r

@eg
def _num1():
   n=num()
   for i in range(1000):
     n + i
     if i % 100 == 0: print(n)
   assert n.n == 1000

@eg
def _num2():
  n = num(i for i in range(901))
  print(n)
  assert n.n == 901

@eg
def _num3():
  x = num()
  for _ in range(10**5):
    x + r()
  x=num([96, 104, 126, 134, 140])
  assert round(x.sd(),3) == 19.131
  assert x.n == 5

if __name__ == "__main__": eg()
```

