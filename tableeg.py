from eg    import eg
from rx    import rx,showrx,say,watch,dominates,watched,printm,freshFile
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

@eg
def _dis1(f="data/china.csv"):
  t=table(file=f)
  for i,r in enumerate(t.rows):
    print("")
    print(i,r)
    print(t.nearest(r,details=True))
    print(t.furthest(r,details=True))


from random import random,shuffle,choice
import collections,nerror
from median import median

@eg
def _knn2(): _knn1("data/maxwell.csv")
@eg
def _knn3(): _knn1("data/nasa93-dem.csv")
@eg
def _knn4(): _knn1("data/coc81.csv")
@eg
def _knn5(): _knn1("data/miyazaki94.csv")
@eg
def _knn1(f="data/china.csv"):
  def xs(lst)       : return [x for _,x in lst]
  def med(lst)  : return median(xs(lst))
  def mu(lst)    : return sum(xs(lst))/ len(lst)
  def late(lst,n=1): 
    nom = [klass/((d+1e-32)**n) for d,klass in lst]
    denom=[1    /((d+1e-32)**n) for d,_     in lst]
    return sum(nom)/sum(denom)
  def late2(lst): return late(lst,2)
  def experiment(klass=None):
    for rx1 in rx(table,
                  K=[1,2,4,8],
                  W= [med,mu,late,late2]):
      for rx2 in rx(num,
                    NORMALIZE=[False,True]):
          log = nerror.nerror()
          t   = table(file=f)
          shuffle(t.rows)
          for row in t.rows[::5]:
              log(actual = t.klass(row),
                  predict= t.knnNum(row))
          s = log.scores()
          yield dict(mmre=s.mmre, mdmre = s.mdmre, se=s.se, Pred25=s.pred25,
                     Corr=s.corr),showrx([rx1,rx2])
  where = freshFile()
  for _ in watch(experiment, where, repeats=5): pass
  #where="/Users/timm/tmp/eg_j61f6q"
  results = watched(where)
  keys=results[0][0].keys()
  betters= [(max if x.istitle() else min) for x in keys]
  tree = lambda: collections.defaultdict(tree)
  xy   = tree()
  for obj,what in enumerate(keys):
    print("\n")
    seen = {}
    for obs,control in results:
      this = control
      seen[this] = seen.get(this,[]) + [obs[what]]
    ranks=[]
    for i,rng in enumerate(scottknot(seen)):
      y,has = rng["y"],rng["has"]
      for x in has:
        this = x[0].label
        xy[this][obj] = i
      ranks += [ (  ' '.join([x[0].label for x in has]), y.all) ]
    for rank,((a,b,c),d) in enumerate(xtiles(ranks,ntiles=4,rnd=0)):
      print(a,c,"=", what+"."+str(rank))
  tmp = []
  for k1 in xy:
    new = [k1]
    for k2 in xy[k1]:
      new += [xy[k1][k2]]
    tmp += [new]
  report = [["wins","rx"] + [(">" if key.istitle() else "<")+key for key in keys]]
  for win,lst in dominates(tmp, betters=betters):
	  report += [[win,lst[0]] + lst[1:]] 
  print("")
  printm(report) 
  print(where)

@eg
def _knn(f="data/diabetes.csv"):
  def w1(w): return w
  def w2(w): return 1/w
  def w3(w): return (1/w)**2
  def experiment(klass):
    for rx1 in rx(table,
                  K=[1,3,5,7],
                  W= [w1,w2,w3]):
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
      print(a,c,"=",what,"", d)
  tmp = []
  print(betters)
  print(keys)
  for k1 in xy:
    new = [k1]
    for k2 in xy[k1]:
      new += [xy[k1][k2]]
    tmp += [new]
  for x in dominates(tmp, betters=betters):
    print(x)

if __name__ == "__main__" : eg()
