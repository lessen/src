from num import *
from eg import eg
from numbers import *
from thing import thing
import time


@eg
def _different(m=512):
  rseed(17)  
  times={}
  for sd0 in range(0,10,2):
    sd = sd0/5
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
              p1.hedges, p1.ttest,p1.same_HT]:
      name = f.__name__
      for n in sorted(pops.keys()):
        rseed(17)
        p0 = pops[n]
        time1 = time.time()
        tmp = f(p0)
        time2 = time.time()
        times[name] = times.get(name,0) + time2 - time1
        print(" * " if tmp else "   ",end=" ")
      print(" : ",name)
  times = sorted([(v,f) for f,v in times.items()])
  for v,f in times:
    print(int(v)+1,"\t",1+int(v/times[0][0]),"\t",f)
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

if __name__ == "__main__": eg()
