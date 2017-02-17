#!/usr/bin/env pypy3
# /* vim: set filetype=python ts=2 sw=2 sts=2 et : */
"""
S.M.O.R.E. = simple multi-objective rule engine.

hello

- Inspired by the Hyperband optimizer: discover good ideas
  by recursively discarding half the bad ones.
- Scores rows by their cdom score.
       - Do this only once then reuse the score.
- OUT = []
- Repeat on training data.
     - BEFORE = cdom distribution of current rows
     - Using cdom score, divide current rows into 50% best and rest.
     - Discretize numerics above and below median using the ranges in the current rows
     - Rank ranges in descending order by b^2/(b+r) where "b" is best and "r" is rest
          - TMP = upper half of the ranges
          - OUT = TMP + OUT # i.e. prepend them in sorted order
     - Discard rows that have none of TMP
     - If too few remaining rows
         exit
     - AFTER = cdom distribution of surviving rows
     - If  cliffsDelta says BEFORE == AFTER
         exit
- Report:
     - A decision ordering diagram running OUT over a test set

Note that the above incrementally discretizes, but only within zones of interest.

Todo: not linear, but clustering remaining rows and explore trees, not a line.
But not too worried about that. The SWAY experience is that most of the solutions
come from a small region.

## Todo

docs strings first line are the summary. but if you go smore help fun then you get
the whole doc

make all data a class. have superclass methods for swapping, removing columns by name
then they get converted into integers which the super class methods fiddle.

have one data class that reads data from strongs

"""

import traceback,sys,re,math,random,time,ast,inspect,subprocess

__author__ = "Tim Menzies"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT, v2"
__version__ = "0.1"
__email__ = "tim@menzies.us"

# Data definitions
# ################

# rule: function(function(x)) == function(x)
def L(x) : return math.log(float(x)) if isinstance(x,str) else x
def F(x) : return float(x)
def S(x) : return x
def I(x) : return int(x)
def X(_) : return "?"

def NUM(x): return x in [L,F,I]

def C(s,sep  = r"\S+",
        dirt = r'([\n\r\t]|#.*)'):
  "Convert a string of words into a list"
  clean = re.sub(dirt, "",s)
  cells = re.findall(sep,clean)
  return [ cell.strip() for cell in cells ]

def CC(s,
       sep  = r"\S+",
       dirt = r'([\n\r\t]|#.*)'):
  return [ C(y) for y in
           [x.strip() for x in
             s.splitlines()]
             if y]

# ____________________________________________________________________________________
#### Data

# todo: if they want to optimize for recent projects, need to max year... how would that change things?

#tod:
  # make class a faracde for the data
  # add strigns as class vars
  # add a superclass that knows how to wipe and swap

def nasa93():
  return dict(
  names=[
     "recordnumber", "projectname", "cat2", "forg", "center", "year", "mode",
     "rely", "data", "cplx", "time", "stor", "virt", "turn", "acap", "aexp",
     "pcap", "vexp", "lexp", "modp", "tool", "sced",
     "equivphyskloc", "act_effort"],
  types=[
X, S,  S,                 S,S,I,   S,           S,S,S,S,S,S,S,S,S,S,S,S,S,S,S,F,   F],
  data= CC("""
1  de  avionicsmonitoring g 2 1979 semidetached h l h n n l l n n n n h h n l 25.9 117.6
2  de  avionicsmonitoring g 2 1979 semidetached h l h n n l l n n n n h h n l 24.6 117.6
3  de  avionicsmonitoring g 2 1979 semidetached h l h n n l l n n n n h h n l 7.7 31.2
4  de  avionicsmonitoring g 2 1979 semidetached h l h n n l l n n n n h h n l 8.2 36
5  de  avionicsmonitoring g 2 1979 semidetached h l h n n l l n n n n h h n l 9.7 25.2
6  de  avionicsmonitoring g 2 1979 semidetached h l h n n l l n n n n h h n l 2.2 8.4
7  de  avionicsmonitoring g 2 1979 semidetached h l h n n l l n n n n h h n l 3.5 10.8
8  erb avionicsmonitoring g 2 1982 semidetached h l h n n l l n n n n h h n l 66.6 352.8
9  gal missionplanning    g 1 1980 semidetached h l h xh xh l h h h h n h h h n 7.5 72
10 gal missionplanning    g 1 1980 semidetached n l h n n l l h vh vh n h n n n 20  72
11 gal missionplanning    g 1 1984 semidetached n l h n n l l h vh h n h n n n 6  24
12 gal missionplanning    g 1 1980 semidetached n l h n n l l h vh vh n h n n n 100 360
13 gal missionplanning    g 1 1985 semidetached n l h n n l l h vh n n l n n n 11.3 36
14 gal missionplanning    g 1 1980 semidetached n l h n n h l h h h l vl n n n 100 215
15 gal missionplanning    g 1 1983 semidetached n l h n n l l h vh h n h n n n 20  48
16 gal missionplanning    g 1 1982 semidetached n l h n n l l h n n n vl n n n 100 360
17 gal missionplanning    g 1 1980 semidetached n l h n xh l l h vh vh n h n n n 150 324
18 gal missionplanning    g 1 1984 semidetached n l h n n l l h h h n h n n n 31.5 60
19 gal missionplanning    g 1 1983 semidetached n l h n n l l h vh h n h n n n 15  48
20 gal missionplanning    g 1 1984 semidetached n l h n xh l l h h n n h n n n 32.5 60
21 X   avionicsmonitoring g 2 1985 semidetached h l h n n l l n n n n h h n l 19.7 60
22 X   avionicsmonitoring g 2 1985 semidetached h l h n n l l n n n n h h n l 66.6 300
23 X   simulation         g 2 1985 semidetached h l h n n l l n n n n h h n l 29.5 120
24 X   monitor_control    g 2 1986 semidetached h n n h n n n n h h n n n n n 15  90
25 X   monitor_control    g 2 1986 semidetached h n h n n n n n h h n n n n n 38  210
26 X   monitor_control    g 2 1986 semidetached n n n n n n n n h h n n n n n 10  48
27 X   realdataprocessing g 2 1982 semidetached n vh h vh vh l h vh h n l h vh vh l 15.4 70
28 X   realdataprocessing g 2 1982 semidetached n vh h vh vh l h vh h n l h vh vh l 48.5 239
29 X   realdataprocessing g 2 1982 semidetached n vh h vh vh l h vh h n l h vh vh l 16.3 82
30 X   communications     g 2 1982 semidetached n vh h vh vh l h vh h n l h vh vh l 12.8 62
31 X   batchdataprocessing g 2 1982 semidetached n vh h vh vh l h vh h n l h vh vh l 32.6 170
32 X   datacapture        g 2 1982 semidetached n vh h vh vh l h vh h n l h vh vh l 35.5 192
33 X   missionplanning    g 2 1985 semidetached h l h n n l l n n n n h h n l 5.5 18
34 X   avionicsmonitoring g 2 1987 semidetached h l h n n l l n n n n h h n l 10.4 50
35 X   avionicsmonitoring g 2 1987 semidetached h l h n n l l n n n n h h n l 14  60
36 X   monitor_control    g 2 1986 semidetached h n h n n n n n n n n n n n n 6.5 42
37 X   monitor_control    g 2 1986 semidetached n n h n n n n n n n n n n n n 13  60
38 X   monitor_control    g 2 1986 semidetached n n h n n n n n n h n h h h n 90  444
39 X   monitor_control    g 2 1986 semidetached n n h n n n n n n n n n n n n 8  42
40 X   monitor_control    g 2 1986 semidetached n n h h n n n n n n n n n n n 16  114
41 hst datacapture        g 2 1980 semidetached n h h vh h l h h n h l h h n l 177.9 1248
42 slp launchprocessing   g 6 1975 semidetached h l h n n l l n n h n n h vl n 302 2400
43 Y   application_ground g 5 1982 semidetached n h l n n h n h h n n n h h n 282.1 1368
44 Y   application_ground g 5 1982 semidetached h h l n n n h h h n n n h n n 284.7 973
45 Y   avionicsmonitoring g 5 1982 semidetached h h n n n l l n h h n h n n n 79  400
46 Y   avionicsmonitoring g 5 1977 semidetached l n n n n l l h h vh n h l l h 423 2400
47 Y   missionplanning    g 5 1977 semidetached n n n n n l n h vh vh l h h n n 190 420
48 Y   missionplanning    g 5 1984 semidetached n n h n h n n h h n n h h n h 47.5 252
49 Y   missionplanning    g 5 1980 semidetached vh n xh h h l l n h n n n l h n 21  107
50 Y   simulation         g 5 1983 semidetached n h h vh n n h h h h n h l l h 78  571.4
51 Y   simulation         g 5 1984 semidetached n h h vh n n h h h h n h l l h 11.4 98.8
52 Y   simulation         g 5 1985 semidetached n h h vh n n h h h h n h l l h 19.3 155
53 Y   missionplanning    g 5 1979 semidetached h n vh h h l h h n n h h l vh h 101 750
54 Y   missionplanning    g 5 1979 semidetached h n h h h l h n h n n n l vh n 219 2120
55 Y   utility            g 5 1979 semidetached h n h h h l h n h n n n l vh n 50  370
56 spl datacapture        g 2 1979 semidetached vh h h vh vh n n vh vh vh n h h h l 227 1181
57 spl batchdataprocessing g 2 1977 semidetached n h vh n n l n h n vh l n h n l 70  278
58 de  avionicsmonitoring g 2 1979 semidetached h l h n n l l n n n n h h n l 0.9 8.4
59 slp operatingsystem    g 6 1974 semidetached vh l xh xh vh l l h vh h vl h vl vl h 980 4560
60 slp operatingsystem    g 6 1975 embedded     n l h n n l l vh n vh h h n l n 350 720
61 Y   operatingsystem    g 5 1976 embedded     h n xh h h l l h n n h h h h n       70  458
62 Y   utility            g 5 1979 embedded     h n xh h h l l h n n h h h h n        271 2460
63 Y   avionicsmonitoring g 5 1971 organic      n n n n n l l h h h n h n l n         90  162
64 Y   avionicsmonitoring g 5 1980 organic      n n n n n l l h h h n h n l n         40  150
65 Y   avionicsmonitoring g 5 1979 embedded     h n h h n l l h h h n h n n n         137 636
66 Y   avionicsmonitoring g 5 1977 embedded     h n h h n h l h h h n h n vl n        150 882
67 Y   avionicsmonitoring g 5 1976 embedded     vh n h h n l l h h h n h n n n        339 444
68 Y   avionicsmonitoring g 5 1983 organic      l h l n n h l h h h n h n l n         240 192
69 Y   avionicsmonitoring g 5 1978 semidetached h n h n vh l n h h h h h l l l        144  576
70 Y   avionicsmonitoring g 5 1979 semidetached n l n n vh l n h h h h h l l l        151  432
71 Y   avionicsmonitoring g 5 1979 semidetached n l h n vh l n h h h h h l l l        34   72
72 Y   avionicsmonitoring g 5 1979 semidetached n n h n vh l n h h h h h l l l        98   300
73 Y   avionicsmonitoring g 5 1979 semidetached n n h n vh l n h h h h h l l l        85   300
74 Y   avionicsmonitoring g 5 1982 semidetached n l n n vh l n h h h h h l l l        20   240
75 Y   avionicsmonitoring g 5 1978 semidetached n l n n vh l n h h h h h l l l        111  600
76 Y   avionicsmonitoring g 5 1978 semidetached h vh h n vh l n h h h h h l l l       162  756
77 Y   avionicsmonitoring g 5 1978 semidetached h h vh n vh l n h h h h h l l l       352  1200
78 Y   operatingsystem    g 5 1979 semidetached h n vh n vh l n h h h h h l l l       165  97
79 Y   missionplanning    g 5 1984 embedded     h n vh h h l vh h n n h h h vh h      60   409
80 Y   missionplanning    g 5 1984 embedded     h n vh h h l vh h n n h h h vh h      100  703
81 hst Avionics           f 2 1980 embedded     h vh vh xh xh h h n n n l l n n h     32   1350
82 hst Avionics           f 2 1980 embedded     h h h vh xh h h h h h h h h n n       53   480
84 spl Avionics           f 3 1977 embedded     h l vh vh xh l n vh vh vh vl vl h h n 41   599
89 spl Avionics           f 3 1977 embedded     h l vh vh xh l n vh vh vh vl vl h h n 24   430
91 Y   Avionics           f 5 1977 embedded     vh h vh xh xh n n h h h h h h n h     165  4178.2
92 Y   science            f 5 1977 embedded     vh h vh xh xh n n h h h h h h n h     65   1772.5
93 Y   Avionics           f 5 1977 embedded     vh h vh xh xh n l h h h h h h n h     70   1645.9
94 Y   Avionics           f 5 1977 embedded     vh h xh xh xh n n h h h h h h n h     50   1924.5
97 gal Avionics           f 5 1982 embedded     vh l vh vh xh l l h l n vl l l h h    7.25 648
98 Y   Avionics           f 5 1980 embedded     vh h vh xh xh n n h h h h h h n h     233  8211
99 X  Avionics            f 2 1983 embedded     h n vh vh vh h h n n n l l n n h      16.3 480
100 X Avionics            f 2 1983 embedded     h n vh vh vh h h n n n l l n n h      6.2  12
"""))

# ______________________________________________________________________-----
#### Rows

class Row:
  """
  Rows are pairs of raw and cooked data.
  Rows know which cells are decisions and objectives.
  For the objectives, rows also know which cells need
  to minimized or maximized.
  """
  def __init__(i,raw=None):
    i.raw, i.cooked,i.rank, i._rowScore = raw, None,0, None
  def __repr__(i):
    return str(i.cooked if i.cooked else i.raw)
  def decs(i,lst): pass
  def objs(i,lst): pass
  def betters(i):  pass
  def ranges(i,cols):
    for col,rng in zip(cols,i.cooked):
      if col.isDecision:
        if rng.val != '?':
          if rng.val in col.ranges:
            yield col,rng
  def rangeScore(i,cols,bests,rests,best=True):
    for _,rng in i.ranges(cols):
      if best: rng.b += 1/bests
      else:    rng.r += 1/rests
  def rowScore(i,cols):
    if i._rowScore is None:
      i._rowScore = 0
      for _,rng in i.ranges(cols):
        i._rowScore += math.log(rng.score()+1e-32,2)
    return i._rowScore

class Classifier(Row):
  """
  Standard row for Classifiers. Last cell is the
  klass.
  """
  def decs(i,lst): return lst[:-1]
  def objs(i,lst): return [lst[-1]]
  def betters(i):  return [min]

class Nklass(Row):
  """
  Standard row for Moea problems.
  Rows can be compared with `cdom`.
  """
  def __init__(i,*lst,**d):
    super().__init__(*lst,**d)
    i.score=0
  def cdom(i, j): # need to normalize
    def w(better):
      return -1 if better == min else 1
    def expLoss(w,x1,y1,n):
      return -1*2.71828**( w*(x1 - y1) / n )
    def loss(x, y):
      losses= []
      n = min(len(x),len(y))
      for z,bt in enumerate(i.betters()):
        x1, y1  = x[z]  , y[z]
        losses += [expLoss( w(bt),x1,y1,n)]
      return sum(losses) / n
    x = i.objs(i.cooked)
    y = j.objs(j.cooked)
    assert len(x) == len(y), "can't compare apples and oranges"
    l1= loss(x,y)
    l2= loss(y,x)
    return l1 < l2

class Coco(Nklass):
  """
  My Cocomo rows are an Moea where
  we want to max/min LOC/effort
  (which are found in the last 2 Columns.
  """
  def decs(i,lst): return lst[:-2]
  def objs(i,lst): return lst[-2:]
  def betters(i):  return [max,min]

## todo: check: can we define the standard Moea problems (e.g. fonseca) as rows?

# ______________________________________________________________________-----
#### Columns

class Column:
  """
  Columns know how to compile raw values for
  that Column, and  how to cook those values.
  They als can keep summary statistics
  for each Column.
  """
  def __init__(i,pos,type):
    i.pos = pos
    i.isDecision = True
    i.type = type
    i.ranges={}
  def raw(i,x)  : return i.type(x)
  def cook(i,val,row):
    if val not in i.ranges:
      i.ranges[val] = Range(i.pos,val)
    r = i.ranges[val]
    r + row
    return r

class SymColumn(Column):
  """
  Symbol Columns are nothing special.
  """
  pass

class NumColumn(Column):
  """
  Numeric Columns know how to chop values
  above and below the median value, and
  how to normalize numbers 0..1 min..max
  """
  def __init__(i,*lst):
    super().__init__(*lst)
    i.lo, i.hi, i.all = 1e31, -1e31, []
    i._median = None
  def raw(i,x):
    x = i.type(x)
    i._median = None # old median now expired
    i.lo = min(i.lo,x)
    i.hi = max(i.hi,x)
    i.all += [x]
    return x
  def median(i): # maintains a cache of the median value
    if i._median is None:
      i._median= median(i.all)
    return i._median
  def cook(i,x,row):
    if i.isDecision:
      val = i.chop(x)
      return super().cook(val,row)
    else:
      return i.norm(x)
  def chop(i,x):
    return "-" if x <= i.median() else "+"
  def norm(i,x):
    return max(0,
               min(1,
                   (x - i.lo)/(i.hi - i.lo + 1e-31)))

# ranges have toself isntall
class Range:
  def __init__(i,pos,val):
    i.pos,i.val  = pos,val
    i.rows = []
    i.b, i.r = 0,0
  def score(i):
    return i.b**2/(i.b + i.r + 1e-32)
  def useful(i):
    return i.b > i.r
  def __add__(i,x):
    i.rows += [x]
    return x
  def __lt__(i,j):
    return i.score() < j.score()
  def __repr__(i):
    return i.val

# _____________________________________________________________________-----
#### Tables

class Table:
  """
  Tables contain Columns and rows.
  Tables organize collecting raw data, then  cook it.
  """
  def __init__(i,names= [],
               types= [],
               data=  [],
               ako =  Classifier):
    i.names = names
    i.types = types
    i.ako   = ako
    i.rows  = []
    # pass0. collect meta data
    i.cols  = [ (NumColumn if NUM(t) else SymColumn)(n,t)
                for n,t in enumerate(types) ]
    for x in ako().objs(i.cols):
      x.isDecision = False
    # pass1: collect data about each Column, create "raw" rows
    for row in data:
      row    = ako([col.raw(val) for col,val in zip(i.cols,row)])
      i.rows += [row]
    # pass2: use what we know about each Column to "cook" the raw values
    for row in i.rows:
      row.cooked = [col.cook(val,row) for col,val in zip(i.cols,row.raw)]

  def clone(i,rows=None):
    rows = rows or i.rows
    return i.__class__(names = i.names,
                 types = i.types,
                 data  = [row.raw[:] for row in rows],
                 ako   = i.ako)

  def scores(i):
    return [x for x in  
            zip(*[row.objs(row.raw) 
                  for row in i.rows])]

class Moea(Table):
  """
  Moea Tables score each row by their cdom score.
  """
  def __init__(i,**options):
    super().__init__(**options)
    i.bests, i.rests = [],[]
  def rankRows(i):
    "score each row according to how many other rows they dominate"
    for row1 in i.rows:
      for row2 in i.rows:
        if row1.cdom(row2):
          row1.score += 1
    i.rows = sorted(i.rows,
                    key=lambda z: z.score,
                    reverse=True)
    for n,row in enumerate(i.rows):
      row.rank = n
    return i.rows
  def score(i):
    m = len(i.rows)
    bests = m // 2
    for n,row in enumerate(i.rankRows()):
      row.rangeScore(i.cols, bests, m - bests, n<= bests)
    tmp = sorted([rng for col in i.cols for rng in col.ranges.values()],reverse=True)
    m = len(tmp)
    i.bests , i.rests = tmp[:m], tmp[m:]
    return i.clone(sorted(i.rows,key=lambda z:z.rowScore(i.cols),reverse=True)[:bests])

    # ______________________________________________________________________-
#### some utilities
def median(lst):
  n = len(lst)
  p = q  = n//2
  if n < 3:
    p,q = 0, n-1
  else:
    lst = sorted(lst)
    if not n % 2: q = p -1
  return lst[p] if p==q else (lst[p]+lst[q])/2

#[["n","a","b"]
# [44,[1,2,2,1,3],[2,2,2]]]

def timeline(lsts):
  def norm(x,n):
    return round(100* (x - lo[n])/(hi[n] - lo[n] + 1e-32)) 
  def medianIQRs(lst):
    lst = sorted(lst)
    q   = len(lst) //4
    return lst[2*q], lst[3*q] - lst[q]
  def norms(lsts):
    lo,hi,out= {},{},[]
    for row in lsts[1:]:
      for n,vals in enumerate(row[1:]):
        lo0   = lo.get(n, 1e32)
        hi0   = hi.get(n,-1e32)
        lo[n] = min(lo0, *vals)
        hi[n] = max(hi0, *vals)
    for row in lsts[1:]:
      for n,vals in enumerate(row[1:]):
        row[n] = [norm(val,n) for val in vals]
    return lsts
  tmp=["#"]
  for x in lsts[0]: 
    tmp += [x,"q","r"]
  out += [tmp]
  befores={}
  ranks={}
  lsts = norms(lst)
  for row in lsts[1:]:
    tmp = [row[0]]
    for n,after in enumerate(row[1:]):
      before= befores.get(n,list())
      if changed(after,before):
        ranks[n] = ranks.get(n,0) + 1
        befores[n] = after
      else:
        before += after
        befores[n] = before
    med,iqr = medianIQR(after)
    tmp += [[med,iqr,ranks.get(n,0)]]
    out += [tmp]
  printm(out)

def changed(lst1,lst2,trivial= [0.147,0.33,0.474][0]):
  "Tests for non-trivial changes between 2 lists."
  lt=gt=n=0
  for x in lst1:
    for y in lst2:
      n += 1
      if x > y: gt +=1
      if x < y: lt +=1
  return (abs(gt-lt) / (n + 1e-32)) > trivial

def printm(matrix,sep=",",align=">"):
  "Pretty print. Columns right justified"
  s = [[str(e) for e in row] for row in matrix]
  lens = [max(map(len, col)) for col in zip(*s)]
  sep = '%s ' % sep
  fmt0 = '{{:%s{}}}' % align
  fmt = sep.join(fmt0.format(x) for x in lens)
  for row in [fmt.format(*row) for row in s]:
    print(row)

def literal(x):
  try:
    return ast.literal_eval(x)
  except Exception:
    return x

def comLine2Dictionary():
  d,pairs={},[]
  for x in sys.argv[2:]:
    if   x[0] == "-": d[re.sub('^-*',"",x)] = False
    elif x[0] == "+": d[re.sub('^\+*',"",x)] = True
    else            : pairs += [x]
  str= ' '.join(pairs)
  NE = r'[^=]+'
  BS = r'\S+'
  tokens = '(' + NE +  ')=('+ '|'.join([BS]) + ')[ \n]*'
  pat= re.compile(tokens)
  d.update({key:re.sub("_",' ',literal(val))
            for (key,val) in re.findall(pat,str) })
  return d

def cmdOLD(*coms):
  pipe=subprocess.PIPE
  run=subprocess.check_output
  for com in coms:
    try:
       print(com)
       #run(com, stdout=PIPE, stderr=PIPE, universal_newlines=True)
       run(com,shell=True,stdin=pipe)
    except Exception:
      pass

def cmd(*cmds):
  for cmd1 in cmds:
    run = subprocess.Popen(cmd1, close_fds=True, shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
      out = run.stdout.read(1)
      if not out:
         break
      sys.stdout.write(out.decode("utf-8"))
      sys.stdout.flush()

# ______________________________________________________________________-
#### demo stuff

def examples(fun=None, group=None, want=None,
             dic={}, groups={},all={},names=[]):
  "Decorator for functions that can be called from command line."
  # ------------------------------------------
  group = group or "__all__"
  def runAll(what):
    n=y=0
    for name in what:
      try:
        run1(all[name])
        y += 1
      except Exception:
        n += 1
        print(traceback.format_exc())
    print("# tried= ",y+n," %passed= ",100*round(y/(y+n)))
  def run1(fun):
    hdr = "\n-----| %s |"+ ("-"*40)
    print(hdr % fun.__name__,end="\n# ")
    if fun.__doc__:
      print(re.sub(r'\n[ \t]*',"\n# ",fun.__doc__))
    print("")
    t1=time.process_time()
    fun(**dic)
    t2=time.process_time()
    print("# pass","(%.4f secs)" % (t2-t1))
    # ------------------------------------------
  def help1(name, doc=' ',defaults=' '):
    fun = all[name]
    if fun.__doc__:
      doc = re.sub(r'\n[ \t]*'," ",fun.__doc__)
    meta= inspect.getargspec(fun)
    if meta.args:
      defaults = ' '.join([('%s=%s' % kv) for kv in
                           zip(meta.args,meta.defaults)])
    return [name,doc,defaults]
  # ------------------------------------------
  if fun:
    txt = fun.__name__
    all[txt] = fun
    names += [txt]
    groups[group] = groups.get(group,list()) + [txt]
  # ------------------------------------------
  elif want : # run one example
    if   want in groups : runAll(groups[want])
    elif want in all    : run1(all[want])
    else                : return print("# %s unknown" % want)
  # ------------------------------------------
  else:
    print("\nSMORE v1: simple multi-objective rule engine")
    print("Copyright (c) 2017, Tim Menzies, tim@menzies.us, MIT license, v2\n")
    print("USAGE: ./smore action [arguments]\n")
    lst= [["action", " ", "arguments"]] +[
          ["------", " ", "--------"]] +sorted([
          help1(name) for name in names]) + [
         ["!", "run all commands", " "]]
    printm(lst, sep="\t", align="<")
  return fun

def eg(x):
  return  examples(fun=x,group="EG")
def shortcut(x):
  return examples(fun=x,group="SHORTCUT")


### and here are the demos that can be called at the command line

@shortcut
def who(email="tim@menzies.us", name="Tim Menzies"):
  "identify yourself to git"
  cmd("git config --global user.email '%s'" % email,
      "git config --global user.name  '%s'" % name,
      "git config --global credential.helper cache",
      "git config credential.helper 'cache --timeout=3600'")

@shortcut
def hello():
  "Update local repo from web"
  cmd("git pull origin master")

@shortcut
def bye():
  "Update web repo from local"
  cmd("git add .",
      "git commit -am newStuff",
      "git push origin master")

@eg
def eg0():
  "basic test, simple classifier"
  t = Table(**nasa93())
  printm([row.cooked for row in t.rows])
  print(t.rows[-4].raw)
  print(t.rows[-4].cooked)

@eg
def eg1():
  "can we handle multi-obj?"
  t = Moea(ako=Coco,**nasa93())
  t.rankRows()
  printm([row.cooked for row in t.rows])

def half(lst):
  n = len(lst)//2
  return median(lst[:n]), median(lst[n:])

def havler(t):
  out  = t.ako().objs(i.names)
  out += [t.scores()]
  while len(t.rows) > 5:
    t = t.score()
    out += [t.scores()]
  return out


@eg
def eg2():
  out= halver(Moea(ako=Coco,**nasa93()))

@shortcut
def doc(module="smore"):
  "Print code documentation"
  cmd("cp %s /tmp/%s.py" % (module,module),
      "(cd /tmp &&  pydoc3  %s)" % module)
# ______________________________________________________________________-
#### main

if __name__ ==  "__main__":
  if len(sys.argv) > 1 and sys.argv[1]:
    examples(want=sys.argv[1],
             dic=comLine2Dictionary())
  else:
    examples()

