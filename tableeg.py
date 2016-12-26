from eg    import eg
from table import table

@eg
def _table1(f="data/weather.csv"):
  t=table(file=f)
  i = 0
  for row in t.rows:
    if i % 1000 == 0:
      print(i)
    i += 1
    pass #print(">>",row)

@eg
def _table2():
  _table1("data/weatherLarge.csv")
  
if __name__ == "__main__" : eg()
