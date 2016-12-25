from eg        import eg
from random    import random as r
from bootstrap import bootstrap as boo
from time      import process_time as now

@eg
def _b0(n=500,div=5, same=None):
  base = [(r()**2)*10 + (r()**0.5)*10 for _ in range(n)]
  print([round(x,2) for x in sorted(base)[::5]])
  same0 = None
  t0 = None
  for b in [30,60,120,240,480, 960]:
    report=["."]*10
    t=0
    for n in range(0,10,1):
      other = [x+ (r()*n/div) for x in base]
      t1    = now()
      same  = boo(base, other,b=b)
      same0 = same if same0 == None else same0
      t2    = now()
      t    += t2 - t1
      if same: report[n] = "="
    t0 = t if t0 == None else t0
    print(''.join(report),dict(b=b,time=round(t/t0,5)))
  assert same0 and not same
         
if __name__ == "__main__": eg()
