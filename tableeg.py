from eg    import eg
from rx    import rx,rx1,say,watch,cdom
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
  def experiment(klass):
    for rx1 in rx(table,
                  K=[1,2,3,4,5],
                  W= [w1,w2]):
      for rx2 in rx(num,
                    NORMALIZE=[True,False]):
          log = abcd()
          t   = table(file=f)
          shuffle(t.rows)     
          for row in t.rows[:30]: 
              log(actual = t.klass(row),
                  predict= t.knn(row))
          s = log.scores()[klass]
          yield dict(acc=s.acc,pd=s.pd,pf=s.pf, prec=s.prec),rx1,rx2
        
    
  results=[x for x in watch(experiment,
                            klass="tested_positive",
                            repeats=30)]
  keys=results[0][0].keys()
  betters= [(min if x=="pf" else max) for x in keys]
  tree = lambda: collections.defaultdict(tree)
  xy   = tree()
  for obj,what in enumerate(keys):
    print("")
    seen = {}
    for obs,*control in results:
      this = rx1(control)
      seen[this] = seen.get(this,[]) + [obs[what]]
    ranks=[]
    for i,rng in enumerate(scottknot(seen)):
      y,has = rng["y"],rng["has"]
      for x in has:
        this = x[0].label
        xy[this][obj] = i
      ranks += [ (  ' '.join([x[0].label for x in has]), y.all) ]
    for (a,b,c),d in xtiles(ranks,rnd=0):
      print(a,c,":",what,":", d)
  tmp = []
  print(betters)
  print(keys)
  for k1 in xy:
    new = [k1]
    for k2 in xy[k1]:
      new += [xy[k1][k2]]
    tmp += [new]
  for x in cdom(tmp, betters=betters):
    print(x)
  
if __name__ == "__main__" : eg()
