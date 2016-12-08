from num import *
from eg import ok
from numbers import *
from thing import thing

@ok
def _num():
  x = num()
  for _ in range(10**5):
    x.add(r())
  x=thing([96, 104, 126, 134, 140])
  assert round(x.my.sd(),3) == 19.131
  assert x.n == 5

@ok
def _different(m=128):
  rseed(13)
  pops = {}
  for n0 in range(2,20):
    n=n0/10
    pops[n] = thing([r()*n for x in range(m)])

  p1 = pops[1.0]
  for f in [p1.cliffsDelta,p1.hedgesTest, p1.ttest,p1.same]:
    print("\n")
    for n in sorted(pops.keys()):
      print(n,end=" ")
    print(f.__name__)
    for n in sorted(pops.keys()):
      p0 = pops[n]
      print("===" if f(p0) else "   ",end=" ")
