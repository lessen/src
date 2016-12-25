from eg        import eg
from random    import random as r
from bootstrap import bootstrap as bst
from time      import process_time as now
import random

def base0(n):
  return [r() for _ in range(n)]

@eg
def _b0(n=50,div=100, boo=bst,same=None,f=base0):
  print(boo.__name__)
  base = f(n)
  print([round(x,2) for x in sorted(base)[::5]])
  same0 = None
  t0 = None
  other=None
  for conf in [60,95]:
    for b in [30,120,480,960]:
      report=[]
      t=0
      for n in range(0,10,1):
        other   = [x+ (r()*n/div) for x in base]
        t1      = now()
        same    = boo(base, other,b=b,conf=conf)
        same0   = same if same0 == None else same0
        t2      = now()
        t      += t2 - t1
        report += ["=" if same else "."]
      t0 = t if t0 == None else t0
      print(''.join(report),dict(conf=conf,b=b,time=round(t/t0,2)))
  print([round(x,2) for x in sorted(other)[::5]])
  assert same0,"first must be the same"
  assert not same,"last should be different"
        
@eg
def _b1():
  for _ in range(10):
    print("")
    k = 0.5+r()*5
    
    print(k)
    f = lambda n: [random.weibullvariate(1,k)
                   for _ in range(n)]
    _b0(f=f)
  
  
if __name__ == "__main__": eg()
