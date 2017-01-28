from eg import eg
from xtile import xtiles,xtile
from random import random as r


@eg
def _xtile1():
 tiles, nums, table = xtile(r() for _ in range(1000))
 print("pretty",tiles,table)
 print("raw   ",nums)

@eg 
def _xtile2():
  n = 100000
  s1= "s1",[r()**4/2      for _ in range(n)]
  s2= "s2",[r()**2        for _ in range(n)]
  s3= "s3",[r()**0.5*1.5  for _ in range(n)]
  s4= "s4",[r()**0.5*0.33 for _ in range(n)]
  for (a,b,c),d in xtiles([s1,s2,s3,s4]):
    print(a,c,":",d)

if __name__ == '__main__':
      eg()
