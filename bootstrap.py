"""
Returns true if two lists are not statistically significantly different.
 
____

## Programmer's Guide
"""
import random
  
def bootstrap(y0,z0, b = 1000, conf= 95):
  tiny=1e-32 # added to add divisions to stop div zero errors
  def testStatistic(y,z): 
    tmp1 = tmp2 = 0
    for y1 in y.all: tmp1 += (y1 - y.mu)**2 
    for z1 in z.all: tmp2 += (z1 - z.mu)**2
    s1    = (tmp1 / (y.n - 1 + tiny))**0.5
    s2    = (tmp2 / (z.n - 1 + tiny))**0.5
    delta = abs(z.mu - y.mu)
    if s1+s2:
      delta =  delta/((s1/(y.n + tiny) + s2/(z.n + tiny))**0.5)
    return delta
  # -------------------------
  class num():
    def __init__(i,some=[]):
      i.sum = i.n = i.mu = 0 ; i.all=[]
      for one in some: i.put(one)
    def put(i,x):
      i.all.append(x);
      i.sum +=x; i.n += 1; i.mu = i.sum/(i.n + tiny)
    def __add__(i1,i2): return num(i1.all + i2.all)
  # -------------------------
  def sampleWithReplacement(lst):
    def any(n)  : return random.uniform(0,n)
    def one(lst): return lst[ int(any(len(lst))) ]
    return [one(lst) for _ in lst]
  # -------------------------
  y, z   = num(y0), num(z0)
  x      = y + z
  tobs   = testStatistic(y,z)
  yhat   = [y1 - y.mu + x.mu for y1 in y.all]
  zhat   = [z1 - z.mu + x.mu for z1 in z.all]
  bigger = tiny
  for i in range(b):
    if testStatistic(num(sampleWithReplacement(yhat)),
                     num(sampleWithReplacement(zhat))) > tobs:
      bigger += 1
  return (bigger / b) > (1 - conf/100)

