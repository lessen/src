from eg    import eg
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

@eg
def _knn(f="data/diabetes.csv"):
  old = num.NORMALIZE
  for k in [1,2,3,4,5]:
    for norms in [True,False]:
      num.NORMALIZE = norms
      print("")
      t= table(file=f)
      log=abcd(db=f,rx=(norms,k))
      for row in t.rows:
        log(actual=t.klass(row),
            predict=t.knn(row,k=k))
      log.report()
  num.NORMALIZE = old

  
if __name__ == "__main__" : eg()
