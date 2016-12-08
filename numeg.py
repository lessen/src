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
def _different(m=512):
  rseed(13)
  for sd0 in range(0,10,2):
    sd = sd0/2
    one = lambda z: r()*z + (-1 if r() <0.5 else 1)*random.gauss(0,sd)
    print("")
    pops = {}
    for n0 in range(0,20,2):
      n       = n0/10
      pops[n] = thing([one(n) for _ in range(m)])
    p1 = pops[1.0]
    for n in sorted(pops.keys()):
       print(n,end=" ")
    print(" :  sd = "+str(sd/10))
    for f in [p1.cliffsDelta,p1.bootstrap,p1.same_CD,
              p1.hedgesTest, p1.ttest,p1.same_HT]:
      for n in sorted(pops.keys()):
        p0 = pops[n]
        print(" * " if f(p0) else "   ",end=" ")
      print(" : ",f.__name__)

"""
Output: note that everyone agrees that if
population1 is 1*population2, then they are all the same.

But as pop2 grows more/less than x*population2, then
more and more they are the same. 

Also, as we increase standard deviation, it is more
likely that all the values are the same.

-----| _different |-----------------------

0.0 0.2 0.4 0.6 0.8 1.0 1.2 1.4 1.6 1.8  :  sd = 0.0
                     *                   :  cliffsDelta
                     *                   :  bootstrap
                     *                   :  sureSame
                 *   *   *               :  hedgesTest
                     *                   :  ttest
                     *                   :  same

0.0 0.2 0.4 0.6 0.8 1.0 1.2 1.4 1.6 1.8  :  sd = 0.1
             *   *   *   *   *           :  cliffsDelta
                 *   *   *               :  bootstrap
                 *   *   *               :  sureSame
         *   *   *   *   *   *   *   *   :  hedgesTest
                 *   *   *               :  ttest
                 *   *   *               :  same

0.0 0.2 0.4 0.6 0.8 1.0 1.2 1.4 1.6 1.8  :  sd = 0.2
 *   *   *   *   *   *   *   *   *   *   :  cliffsDelta
                 *   *   *       *       :  bootstrap
                 *   *   *       *       :  sureSame
 *   *   *   *   *   *   *   *   *   *   :  hedgesTest
                 *   *   *               :  ttest
                 *   *   *               :  same

0.0 0.2 0.4 0.6 0.8 1.0 1.2 1.4 1.6 1.8  :  sd = 0.3
 *   *   *   *   *   *   *   *   *   *   :  cliffsDelta
                 *   *   *   *   *       :  bootstrap
                 *   *   *   *   *       :  sureSame
 *   *   *   *   *   *   *   *   *   *   :  hedgesTest
                 *   *   *   *           :  ttest
                 *   *   *   *           :  same

0.0 0.2 0.4 0.6 0.8 1.0 1.2 1.4 1.6 1.8  :  sd = 0.4
 *   *   *   *   *   *   *   *   *   *   :  cliffsDelta
     *   *   *   *   *   *       *   *   :  bootstrap
     *   *   *   *   *   *       *   *   :  sureSame
 *   *   *   *   *   *   *   *   *   *   :  hedgesTest
         *   *   *   *   *               :  ttest
         *   *   *   *   *               :  same
"""
