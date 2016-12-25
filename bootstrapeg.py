from eg        import eg
from random    import random as r
from bootstrap import bootstrap as bst
from time      import process_time as now
import random

def bootstrap1(y0,z0,conf=0.05,b=1000):
  """The bootstrap hypothesis test from
     p220 to 223 of Efron's book 'An
    introduction to the boostrap."""
  def sampleWithReplacement(lst):
    "returns a list same size as list"
    def any(n)  : return random.uniform(0,n)
    def one(lst): return lst[ int(any(len(lst))) ]
    return [one(lst) for _ in lst]

  def testStatistic(y,z): 
    """Checks if two means are different, tempered
     by the sample size of 'y' and 'z'"""
    tmp1 = tmp2 = 0
    for y1 in y.all: tmp1 += (y1 - y.mu)**2 
    for z1 in z.all: tmp2 += (z1 - z.mu)**2
    s1    = (float(tmp1)/(y.n - 1))**0.5
    s2    = (float(tmp2)/(z.n - 1))**0.5
    delta = z.mu - y.mu
    if s1+s2:
      delta =  delta/((s1/y.n + s2/z.n)**0.5)
    return delta
  class total():
    "quick and dirty data collector"
    def __init__(i,some=[]):
      i.sum = i.n = i.mu = 0 ; i.all=[]
      for one in some: i.put(one)
    def put(i,x):
      i.all.append(x);
      i.sum +=x; i.n += 1; i.mu = float(i.sum)/i.n
    def __add__(i1,i2): return total(i1.all + i2.all)
  y, z   = total(y0), total(z0)
  x      = y + z
  tobs   = testStatistic(y,z)
  yhat   = [y1 - y.mu + x.mu for y1 in y.all]
  zhat   = [z1 - z.mu + x.mu for z1 in z.all]
  bigger = 0
  for i in range(b):
    if testStatistic(total(sampleWithReplacement(yhat)),
                     total(sampleWithReplacement(zhat))) > tobs:
      bigger += 1
  return bigger / b > conf

@eg
def _b0(n=500,div=1.5, boo=bst,same=None):
  print(boo.__name__)
  base = [(r()**2)*10 + (r()**0.5)*10 for _ in range(n)]
  print([round(x,2) for x in sorted(base)[::5]])
  same0 = None
  t0 = None
  other=None
  for b in [30,60,120,240,480, 960]:
    report=[]
    t=0
    for n in range(0,10,1):
      other = [x+ (r()*n/div) for x in base]
      t1    = now()
      same  = boo(base, other,b=b)
      same0 = same if same0 == None else same0
      t2    = now()
      t    += t2 - t1
      report += ["=" if same else "."]
    t0 = t if t0 == None else t0
    print(''.join(report),dict(b=b,time=round(t/t0,5)))
  print([round(x,2) for x in sorted(other)[::5]])
  assert same0 and not same
        
@eg
def _b1():
  _b0(boo=bootstrap1)

if __name__ == "__main__": eg()
