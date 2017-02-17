
# nerror

Watch over a learner making numeric predictions.


```python
import sys,re,median,random

class nerror:
  def __init__(i, db="all",rx="rx"):
    i.db = str(db)
    i.rx = rx
    i.log = []

  def __call__(i, actual=None,predict=None):
    i.log += [(actual,predict)]

  def pearson(i,x,y):
    n     = len(x)
    sumx  = sum( [x[i]      for i in range(n)] )
    sumy  = sum( [y[i]      for i in range(n)] )
    sumxSq= sum( [x[i]**2   for i in range(n)] )
    sumySq= sum( [y[i]**2   for i in range(n)] )
    pSum  = sum( [x[i]*y[i] for i in range(n)] )
    num   = n*pSum-(sumx*sumy)
    den   = (n*sumxSq-sumx**2)**.5 * (n*sumySq-sumy**2)**.5
    return 1 if den==0 else num/den

  def header(i):
    print("#"),
    '{0:20s} {1:11s}   {2:4s} {3:4s} {4:4s} {5:4s}{6:4s} '.format( 
      "db","rx","n","re","mmre","mdmre","sa","pred(25)","pred(50)")
    print('-'*100)

  def scores(i):
    # Convenience class. Can acces fields as x.f not x["f"].
    class oo:
      def __init__(i, **adds): i.__dict__.update(adds)
    n        = len(i.log)
    mres     = []
    saDenom  = saNom = 0
    pred25   = pred30 = pred50 = 0
    actuals  = [actual for actual,_ in i.log]
    sampled  = sum(random.choice(actuals) for _ in range(1000))/1000
    for actual, predict in i.log:
      ar1 = predict-actual
      re1 = abs(ar1/(actual+1e-32))
      if re1*100 < 25 : pred25 += 1/n
      if re1*100 < 30 : pred30 += 1/n
      if re1*100 < 50 : pred50 += 1/n
      mres    += [re1]
      saNom   += abs(actual - predict)/n
      saDenom += abs(actual - sampled)/n
    return oo(db=i.db, rx=i.rx, 
              mmre = sum(mres) / n * 100,
              mdmre= median.median(mres)*100,
              se   = saNom  / saDenom * 100,
              pred25=pred25*100,
              pred30=pred30*100,
              pred50=pred50*100,
              corr = i.pearson([a for a,_ in i.log],
                               [p for _,p in i.log])*100)
```

