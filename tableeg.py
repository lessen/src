from eg    import eg
from rx    import rx
from table import table
from abcd  import abcd
from num import num

@eg
def _table1(f="data/weather.csv"):
  t=table(file=f)
  i = 0
  for row in t.rows:
    if i % 1000 == 0:
      print(i)
    i += 1
  print(t)
  print(t.group["x"])

@eg
def _table2():
  _table1("data/weather100K.csv")

@eg
def _table3():
  import cProfile
  import re
  cProfile.run('_table2()')

@eg
def _dis(f="data/weather.csv"):
  t=table(file=f)
  for i,r in enumerate(t.rows):
    print("")
    print(i,r)
    print(t.nearest(r,details=True))
    print(t.furthest(r,details=True))
  print(t.distances())  


from random import random,shuffle

@eg
def _knn(repeats=20, f="data/diabetes.csv"):
  def w1(w): return w
  def w2(w): return 1/w
  def w3(w): return (1/w)**2
  def experiment():
    for k in [1,2,3,4,5]:
      for norms in [True,False]:
        for w in [w1,w2,w3]:
          with rx(table,K=k,W=w): # change this to for _ in rx(table,k=[1,2,3],W=[w1,w2,w3]): etc
            with rx(num,NORMALIZE=norms):
                log  = abcd()
                t    = table(file=f)
                shuffle(t.rows)          # this
                for row in t.rows[:100]: # could
                  if random() < 0.2:     #  be a methid
                    log(actual = t.klass(row),
                        predict= t.knn(row,k=k))
                s = log.scores()["__all__"]
                yield (dict(k=k,norms=norms,w=w.__name__),
                       dict(acc=s.acc,pd=s.pd,pf=s.pf, prec=s.prec))
  for x,y in experiment():
    print(x,y)
    
if __name__ == "__main__" : eg()
