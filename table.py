from thing import thing
from csv   import csv

class table:
  id = 0
  WHITESPACE = '[\n\r\t]'
  COMMENTS   = '#.*'
  IGNORE     = "-"
  MISSING    = '?'
  COLS       = dict(less= "<",
                    more= ">",
                    klass=":",
                    nums= "$<>",
                    syms= ":!")       

  def __init__(i,inits=[],file=None,zip=None):
    i.rows, i.cols, i.all = [],{},[]
    for key in table.COLS.keys():
      i.cols[key] = []
    if file:
      for row in i.columns(csv(file=file,zip=zip)):
        print(row)
        i + row
    [i + row for row in i.columns(inits)]
    
  def columns(i,src):
    """Yields just the columns not marked as missing."""
    use=[]
    for row in src:
      use = use or [col for col,cell in enumerate(row)
                        if  cell[0] != table.MISSING ]
      yield [row[col] for col in use]

  def __add__(i,row):
    i.data(row) if i.all else i.header(row)

  def header(i,row):
    for col,cell in enumerate(row):
      print("[%s,%s]" % (col,cell))
      if cell[0] != table.IGNORE:
        column  = thing(pos=col, txt=cell)
        i.all  += [column]
        for key,chars in table.COLS.items():
          for char in chars:
            if cell[0] == char:
              print(char,col,cell)
              i.cols[key] += [column]
          
  def data(i,row):
    class _row:    
      def __init__(i,lst):
        i.id = table.id = table.id+1
        i.raw=lst
      def __repr__(i)       : return '#%s,%s' % (i.id,i.raw)
      def __getitem__(i,k)  : return i.raw[k]
      def __setitem__(i,k,v): i.raw[k] = v
      def __len__(i)        : return len(i.raw)
      def __hash__(i)       : return i.id 
      def __eq__(i,j)       : return i.id == j.id
      def __ne__(i,j)       : return i.id != j.id
    row = [x + row[x.pos] for x in i.all]
    i.rows += [ _row(row) ] 
              
  def dist(i, j,k, what=["syms","nums"]):
    ds,ns = 0,1e-32
    for x in what:
      for y in i.cols[x]:
        d,n  = y.dist(j[y.pos], k[y.pos], table.MISSING)
        ds  += d
        ns  += n
    return ds**0.5 / ns**0.5

