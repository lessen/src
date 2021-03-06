
# table


Given a source of csv data, `table` reads and stores the rows while at the same
time keeping statistics on what was seen in each row.

Column statistics are kept as `thing`s which are instances of a class that
watches a stream of data and works out if that column is a numeric or symbolic.
All these `things` are stored in `table.all` as well as in the _column groups_
defined in `table.COLS`.

       DEFAULT= "x"
       COLS   = dict(less = "<",   # numeric goals to minimize
                     more = ">",   # numeric goals to maximize
                     klass= ":",   # symbolic goal (for classification)
                     y    = ":<>"):# all symbols denoting goals

Any column with a header that starts with something else, get stored in the
group table.DEFAULT.

By default, `table` reads all its data at once from a `inits` list passes to its
constructor. But `table` can also read table rows incrementally from strings, a
file, or a file inside a zip file.

For very fast csv reads, use `csv` not `table`.  `Table` uses `csv` as a
primitive but also keeps extensive statistics on each column.  If those
statistics are not required, then use `csv` for (much) faster loads.  For
example, on one machine, with pypy3, `csv` can load nearly two million records
in under six seconds while in the same time `table` can only load 10,000.

For clues on how to optimize `table`, see the profiler output of `pypy3
tableg.py -- _table3`.

_____
## Programmer's Guide


```python
from thing import thing
from csv   import csv

class table:
  K        = 3
  W        = lambda x:x
  DEFAULT    = "x"
  COLS       = dict(less = "<",   # numeric goals to be minimized
                    more = ">",   # numeric goals to be maximized
                    klass= ":",   # symbolic goal (used for classification)
                    y    = ":<>"  # all symbols denoting goals
                    )             # (any any other thing goes into table.DEFAULT)

  # Read table either from a `str`, a `file`, a `file` in a `zip`
  # or from some `inits` list.
  def __init__(i,inits=[],str=None,file=None,zip=None):
    i.rows, i.group, i.all = [],{},[]
    i.group[table.DEFAULT] = []
    for key in table.COLS.keys():
      i.group[key] = []
    if file:
      for row in csv(str=None, file=file,zip=zip,header=True):
        i + row
    [i + row for row in inits]

  def __repr__(i):
    return '{:rows %s :less %s :more %s :klass %s :x %s :y %s' % (
            len(i.rows),           len(i.group["less"]), len(i.group["more"]),
            len(i.group["klass"]), len(i.group["x"]),    len(i.group["y"]))

  # If `all` is defined, we are beyong the first header row.
  def __add__(i,row):
    i.data(row) if i.all else i.header(row)

  # Create one `thing` for each column.
  # Store that `thing` in `all` as well as
  # in its associated `COLS` group.
  def header(i,row):
    for col,cell in enumerate(row):
      t      = thing(pos=col, txt=cell)
      i.all += [t]
      placed = False
      for key,chars in table.COLS.items():
        for char in chars:
          if cell[0] == char:
            i.group[key] += [t]
            placed = True
      # If we can't place it anywhere else, place it in `table.DEFAULT`.
      if not placed:
        i.group[table.DEFAULT] += [t]

  # Update the statistics held in each thing for each column.
  # Keep the data in `rows`.
  def data(i,row):
    [t + row[t.pos] for t in i.all]
    i.rows += [ row ]

  # ### Misc utilities


  # Return a table just like this one,
  # but withtout the row data
  def twin(i,inits=[]):
    t = table([[t.txt for t in i.all]])
    [t + x for x in inits]
    return t

  # Return the first klass value of a row
  def klass(i,row):
    return row[i.group["klass"][0].pos]

  # Return the first goal value of a row
  def goal(i,row):
    return row[i.group["y"][0].pos]

  # Compute Euclidean distance between two rows.
  # Makes use of sevices defined in each thing in `all`.
  def dist(i, j,k, what=None):
    ds,ns = 0,1e-32
    what = what or [table.DEFAULT]
    for grp in what:
      for t in i.group[grp]:
        d    = t.dist(j[t.pos], k[t.pos])
        if d is not None:
          ds  += d
          ns  += 1
    return ds**0.5 / ns**0.5

  def nearest(i,row,rows=None,what=None,details=False,
              bt   = lambda x,y: x< y,
              zero = 1e32):
    best = zero
    out  = row
    rows = rows or i.rows
    for otherRow in rows:
      if id(row) != id(otherRow):
        tmp = i.dist(row, otherRow,
                     what=what or [table.DEFAULT])
        if bt(tmp,best):
          out,best = otherRow,tmp
    return out,best if details else out

  def furthest(i,row,rows=None,what=None,details=False):
    return i.nearest(row,
                   what = what or [table.DEFAULT],
                   rows = rows or i.rows,
                   bt   = lambda x,y: x > y,
                   zero = -1,
                   details=details)

  def distances(i,rows=None,what=None):
    out,index = {},{}
    rows = rows or i.rows
    for j,row in enumerate(rows):
      out[j] = []
      index[j] = row
    for j,row1 in enumerate(rows):
      for k,row2 in enumerate(rows):
        if j > k:
          d = i.dist(row1,row2,
                     what = what or [table.DEFAULT])
          out[j] += [(d,k)]
          out[k] += [(d,j)]
    for k in out:
      out[k].sort()
    return out,index

  def knnNum(i,row1,k=None,rows=None,w=None):
    k = k or table.K
    w = w or table.W
    rows= rows or i.rows
    tmp = [(i.dist(row1,row2), i.klass(row2))
           for row2 in rows
           if id(row1) != id(row2)]
    kth = sorted(tmp)[:k]
    return w(kth)

  def knn(i,row1,k=None,rows=None,w=None):
    k = k or table.K
    w = w or table.W
    rows=rows or i.rows
    tmp = [(w(i.dist(row1,row2)),
            i.klass(row2))
           for row2 in rows
           if id(row1) != id(row2)]
    kth = sorted(tmp)[:k]
    scores={}
    for w,klass in kth:
      scores[klass] = scores.get(klass,0) + w
    ranked = sorted(scores.items(), reverse=True,key=lambda x: x[1])
    return ranked[0][0]

  def knn(i,row1,k=None,rows=None,w=None):
    k = k or table.K
    w = w or table.W
    rows=rows or i.rows
    tmp = [(w(i.dist(row1,row2)),
            i.klass(row2))
           for row2 in rows
           if id(row1) != id(row2)]
    kth = sorted(tmp)[:k]
    scores={}
    for w,klass in kth:
      scores[klass] = scores.get(klass,0) + w
    ranked = sorted(scores.items(), reverse=True,key=lambda x: x[1])
    return ranked[0][0]

```

