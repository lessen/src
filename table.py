from num import num
from sym import sym

class table:
  WHITESPACE = '[\n\r\t]'
  COMMENTS   = '#.*'
  IGNORE     = "-"
  MISSING    = '?'
  COLS       = dict(less= "<",
                    more= ">",
                    klass=":",
                    nums= "$",
                    syms= "!")
  class _row:
    id = 0
    def __init__(i,lst):
      i.id = row.id = row.id+1
      i.raw=lst
      i.cooked=None
    def _data(i)          : return i.cooked if i.cooked else i.raw
    def __repr__(i)       : return '#%s,%s' % (i.id,i._data())
    def __getitem__(i,k)  : return i._data()[k]
    def __setitem__(i,k,v): i._data()[k] = v
    def __len__(i)        : return len(i._data())
    def __hash__(i)       : return i.id 
    def __eq__(i,j)       : return i.id == j.id
    def __ne__(i,j)       : return i.id != j.id

  def __init__(i,inits=[],file=None.zip=None):
    i.rows, i.cols, i.all = [],{},[]
    for key in table.COLS.keys():
      i.cols[key] = []
    if file:
      for row in csv(file=file,zip=zip):
        i + row

  def __add__(i,row):
    i.header(row) if i.all else i.data(row)

  def header(i,row,pos= -1):
    for col,cell in enumerate(row):
      if cell[0] != table.IGNORE:
        pos += 1
        for key,char in table.COLS.items():
          if cell[0] == char:
            new = thing(pos=pos, get=col txt=cell)
            i.cols[ key ] += [new]
            i.all +=  [new]
            break
          
  def data(i,row):
    row = [x + row[x.get] for x in i.all]
    i.rows += [ _row(row) ] 
              
  def dist(i, j,k, what=["syms","nums"]):
    ds,ns = 0,1e-32
    for x in what:
      for y in i.cols[x]:
        d,n  = y.dist(j[y.col], k[y.col], table.MISSING)
        ds  += d
        ns  += n
    return ds**0.5 / ns**0.5

