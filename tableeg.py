from eg    import eg
from table import table

@eg
def _table():
  t=table(file="data/weather.csv")
  for row in t.rows:
    print(">>",row)

if __name__ == "__main__" : eg()
