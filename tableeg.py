from eg    import eg
from rx    import rx,rx1,say
from table import table
from abcd  import abcd
from num import num
from ranges import ddiv,scottknot
from xtile import xtile,xtiles

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
import collections

@eg
def _knn(f="data/diabetes.csv"):
  def w1(w): return w
  def w2(w): return 1/w
  def w3(w): return (1/w)**2
  def experiment(repeats):
    for rx1 in rx(table,
                  K=[1,2,3,4,5],
#                  W= [w1,w2,w3]):
                  W=w1):
      for rx2 in rx(num,
                    NORMALIZE=[True,False]):
        for r in range(repeats):
          log = abcd()
          t   = table(file=f)
          shuffle(t.rows)          # this
          for row in t.rows[:100]: # could
            if random() < 0.2:     #  be a methid
              log(actual = t.klass(row),
                  predict= t.knn(row))
          s = log.scores()["__all__"]
          yield dict(repeat= r,
                     result= dict(acc=s.acc,pd=s.pd,pf=s.pf, prec=s.prec),
                     rx    = [rx1,rx2])
        
  
  results = [x for x  in experiment(30)]
  for what in ["pd","pf","acc","prec"]:
    seen = {}
    for x in results:
      this = rx1(x["rx"])
      #if x["repeat"]==0: say("\n",this)
      #say(" ", x["repeat"])
      seen[this] = seen.get(this,[]) + [x["result"][what]]
    ranks=[]
    for rng in scottknot(seen):
      y,has = rng["y"],rng["has"]
      ranks += [ (  ' '.join([x[0].label for x in has]), y.all) ]
    for (a,b,c),d in xtiles(ranks,rnd=0):
      print(a,c,":",what,":", d)
    
if __name__ == "__main__" : eg()
