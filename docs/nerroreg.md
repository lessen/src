
# nerroreg

from nerror import nerror
from eg import eg
from random import random as r
from xtile import xtile

@eg
def _nerr():
  log = nerror()
  for n in range(101):
    log(n, n*(1 - r()*0.5))
  tile,_,vals = xtile([100*abs(a-p)/(a+0.0001) for a,p in log.log])
  print(tile,vals)
  s = log.scores()
  assert  round(s.corr,3)   ==  93.285
  assert  round(s.pred30,3) ==  63.366
  assert  round(s.pred50,3) == 100.000
  assert  round(s.se,3)     ==  52.712
  assert  round(s.mdmre,3)  ==  25.421


if __name__ == "__main__": eg()
```

