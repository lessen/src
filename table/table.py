from num import *
from sym import *

class table:
  whitespace = '[\n\r\t]'
  comments   = '#.*'
  sep        = ","
  ignore     = "-"
  missing    = '?'
  cols       = dict(less= ("<", num),
                    more= (">", num),
                    nums= ("$", num),
                    syms= ("=", sym))

  def __init__(i,file=None):
    i.rows,i.cols,i.all = [],{},[]
    i.col2cell, i.cell2col = {}, {}
    for key in table.cols.keys():
      i.cols[key] = []
    if file:
      return i.create(i.lines(file))

  def create(i,src):
    width = None
    for j,line in enumerate(src):
      if j == 0:
        width = len(line)
        i.header(line)
      else:
        assert width == len(line), "wanted %s cells" % width
        i.rows += [ i.compile(line) ]
        
  def compile(i,line):
    for x in i.all:
      y = line[x.col] = x.compile( line[x.col] )
      x.add(y)
    return line
  
  def header(i,line):
    for col,cell in enumerate(line):
      i.col2cell[col] = cell
      i.cell2col[cell] = col
      if cell[0] != table.ignore:
        for key,(char,what) in table.cols.items():
          if cell[0] == char:
            new = what(cell,col)
            i.cols[ key ] = i.cols.get( key, []) + [new]
            i.all += [new]
            break
          
  def lines(i,file):
    doomed = re.compile('(' + table.whitespace + '|' +  table.comments + ')')
    with open(file) as fs:
      cache = []
      for line in fs:
        line = re.sub(doomed, "", line)
        if line:
          cache += [line]
          if line[-1] != ",":
            line  = "".join(cache)
            cache = []
            row   = map(lambda z:z.strip(),  line.split(table.sep))
            if len(row)> 0:
              yield row
              
  def dist(i, j,k, what=["syms","nums"]):
    ds,ns = 0,1e-32
    for x in what:
      for y in i.cols[x]:
        d,n  = y.dist(j[y.col], k[y.col], table.missing)
        ds  += d
        ns  += n
    return ds**0.5 / ns**0.5

