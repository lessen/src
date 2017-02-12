
_Ranges_ implements discretization; i.e.  transform quantitative 
data into qualitative data.  Even for algorithms that can directly 
deal with quantitative data, dscretization can led to faster, 
more effective learning.

It turns out that a generic recursive bi-clustering procedure 
can implement all the following discretization processes:

- Divide a list of numbers into a small number of ranges;
- Given rows of data...
    - Fayyad-Iranni discretization:
          - ... find ranges in one column that 
            minimizes the expected value of the 
            entropy in another column of symbols.
    - CART-style discretization:
          - ... find ranges in one column that 
            minimizes the expected value of the 
            standard deviation in another column of numbers.
    - Scott-Knott ranking of treatments (clustering together 
      treatments whose distributions are statistically
      indistinguishable).

### Examples

#### `div`: Separate a List into Ranges

       from ranges import div
       #
       for rng in div([ 10, 11, 13, 14, 15, 15, 16, 16, 17, 
                        20, 21, 23, 24, 25, 25, 26, 26, 27, 
                        30, 31, 33, 34, 35, 35, 36, 36, 37 
                      ]):
         print("range,rng["id"],":",
                 dict(lo= rng["x"].lo,
                      hi= rng["x"].hi))
       
       # Output
       range 1: {'lo': 10, 'hi': 20} # nums 10 to 20
       range 2: {'lo': 21, 'hi': 31} # nums 21 to 31
       range 3: {'lo': 33, 'hi': 37} # nums 33 to 37

#### `ediv`: Separate pairs of Number,Symbols into Ranges

       from ranges import div,ediv
       # 
       a,b  = "a","b"
       for rng in ediv([ 
                    (10,a),(11,a),(13,a),(14,a),(15,a),
                    (20,b),(21,b),(23,b),(24,b),(25,b),
                    (30,b),(31,b),(33,b),(34,b),(35,b) ]):
          print(dict(id= rng["id"],
                     lo= rng["x"].lo,
                     hi= rng["x"].hi))
        
       # Output
       range 0 : {'lo': 10, 'hi': 20}
       range 1 : {'lo': 21, 'hi': 35}

#### `sdiv`: Separate pairs of Number,Numbers into Ranges

       lst= [( 0.7,  2),  ( 0.75,  2 ), ( 0.8,  2  ),
             ( 0,85 ,2),  ( 0.9,   2),  ( 0.8 ,  2  ),
             ( 1  ,  2 ), ( 1.05 , 2),  ( 1,2),
             ( 0.7,  2),  ( 0.75,  2 ), ( 0.8,  2  ),
             ( 0.85 , 2), ( 0.9,  2),   (10   , 14  ),
             (10.5, 13.5),(11    ,13),  (11.5, 13),  
             (12   , 12.5),(12.5, 12  ),(13    ,11.5),
             (13.5, 10.5),(14   , 10  ),(14.5,  9.5),
             (15    , 9), (15.5, 8.5) ]
       for rng in sdiv(lst):
           print("range",rng["id"],":",
                    dict(lo= rng["x"].lo,
                          hi= rng["x"].hi))
        
       # Output
       range 0 : {'lo': 0,   'hi':  0.9}
       range 1 : {'lo': 0.9, 'hi': 15.5}

#### `ddiv`: Separate lists of Treatment into Ranges

       for rng in ddv(dict(x1= [0.34, 0.49, 0.51, 0.6],
                           x2= [0.6,  0.7,  0.8,  0.9],
                           x3= [0.15, 0.25, 0.4,  0.35],
                           x4= [0.6,  0.7,  0.8,  0.9],
                           x5= [0.1,  0.2,  0.3,  0.4])):   
         print("range", rng["id"],":",
               [x[0].label for x in rng["has"]],
               dict(lo= rng["x"].lo,
                    hi= rng["x"].hi))
      
       # Output
       range 0 : ['x5', 'x3'] {'lo': 0.1,  'hi': 0.4} 
       range 1 : ['x1']       {'lo': 0.34, 'hi': 0.6} 
       range 2 : ['x2', 'x4'] {'lo': 0.6,  'hi': 0.9} 

### Internal Details

`Ranges` assumes that the input data contains a list of doubles _(x,y)_
pairs.  The process assumes _x_ is always numeric, but _y_ may 
be numeric or symbols. 

- If _y_ is _numeric_,  we divide to minimize the expected 
  _variance_ (after divisions).
- If _y_ is _symbolic_, we divide to minimize the expected 
  _entropy_ (after divisions).

To divide a list of numerics, this generates doubles _(x,x)_, 
after which the same division process executes.

However it runs, this ranges returns a list of dictionaries:

         dict(label = label, score = score,
              x     = xoverall, # x.lo, x.hi defines the range 
              y     = yoverall, # could be numerics or symbols
              has   = items,
              id    = aNumber)

____ 

## Programmer's Guide

```python

import sys,math
from cliffsDelta import cd 
from bootstrap   import bootstrap

# ### Top-level drives

# Short-cuts, defined for standard usages.

# Standard usage #1: divide a list of numbers.
def div(lst):
  return ranges(lst)

# Standard usage #2:
def sdiv(lst,
         x   = lambda z:z[ 0],
         y   = lambda z:z[-1],
         key = lambda z:z[ 0]):
  return ranges(lst, key=key, x=x, y=y)

def ediv(lst,
         x   = lambda z:z[ 0],
         y   = lambda z:z[-1],
         key = lambda z:z[ 0]):
  def fayyadIranni(lhs,rhs,all,score):
    gain  = all.ent() - score
    delta = math.log(3**all.k()-2,2) - (all.ke() - lhs.ke() - rhs.ke())
    return gain > (math.log(all.n-1,2) + delta)/all.n
  return ranges(lst,
                ynum=False,
                goodysplit=fayyadIranni,key=key, x=x, y=y)

def scottknot(d):
   def expectedMuChange(lhs,rhs,all):
     return  (lhs.n/all.n * abs(lhs.median() - all.median())**2 + \
       rhs.n/all.n * abs(rhs.median() - all.median())**2)
   def stats(lhs,rhs,_):
     tmp = not cd(lhs.all,rhs.all) and not bootstrap(lhs.all,rhs.all)
     #print(tmp, lhs.all, rhs.all)
     return tmp
   lst=[]
   for k,v in d.items():
     tmp=num(v)
     tmp.label= k
     lst += [tmp]
   return ranges(lst,
                 flat=False,
                 d   = 0.3,
                 x   = lambda z:z.all,
                 y   = lambda z:z.all,
                 goodxsplit = stats,
                 evaly = expectedMuChange,
                 better = lambda new,t,old : new > t*old,
                 score0 = lambda x: -1e31,
                 key = lambda z:z.median())
 

def ddiv(d,f=None):
   lst=[]
   for k,v in d.items():
     tmp=num(v)
     tmp.label= k
     lst += [tmp]
   return ranges(lst,
                 flat=False,
               x   = lambda z:z.all,
               y   = lambda z:z.all,
               key = lambda z:z.median())
  
#-----------------------------------
def ranges(lst,
           d          = 0.3,
           cliffsDelta= 0.147,
           enough     = None,
           enoughth   = 0.71,
           epsilon    = None,
           evaly      = None,
           better     = lambda new,t,old : new * t < old,
           score0     = lambda x: x.wriggle(),
           flat       = True,
           goodxsplit = None,
           goodysplit = None,
           greedy     = True,
           label      = "ranges",
           rnd        = 3,
           trivial    = 1.05, # 1%
           key        = lambda z:z,
           verbose    = False,
           x          = lambda z:z,
           y          = lambda z:z,
           ynum       = True,
          ):
  def expectedWriggle(lhs,rhs,all):
     return lhs.n/all.n * lhs.wriggle() + \
           rhs.n/all.n * rhs.wriggle()
  def yes(*l,**d): return True
  evaly= evaly or expectedWriggle
  goodxsplit = goodxsplit or yes
  goodysplit = goodysplit or yes
  def stats(segment, xall, yall,flat):
     xs,ys = num(),yklass()
     if flat:
       for one in segment:
         x1 = x(one)
         y1 = y(one)
         xs   + x1
         xall + x1
         ys   + y1
         yall + y1
     else:
       for x1 in segment.all:
         xs.label = segment.label
         ys.label = segment.label
         xs   + x1
         xall + x1
         ys   + x1
         yall + x1
     return xs,ys
  #-----------------
  def summary(segments):
    xall,yall=[],[]
    xs, ys  = {},{}
    for i,(x,y) in enumerate(segments[::-1]):
      j    = len(segments) - i - 1
      xall += x.all
      yall += y.all
      newx = num(xall)
      newy = yklass(yall)
      xs[j] = newx
      ys[j] = newy
      #print("!!!",j,newx,newy)
    return xs, ys, num(xall), yklass(yall)
  #-----------------
  def divide(segments, out,lvl, cut=None):
    xrhsall, yrhsall, xoverall, yoverall = summary(segments)
    score, score1 = score0(yoverall), None
    xlhs, ylhs    = num(), yklass()
    for i,(x,y) in enumerate(segments[:-1]):
      xrhs = xrhsall[i+1]
      yrhs = yrhsall[i+1]
      nextx = segments[i+1][0]
      #print("::",i,x,y)
      [xlhs+z for z in x.all]
      [ylhs+z for z in y.all]
      if xlhs.median() + epsilon < nextx.median(): #xrhs.median():
        score1 = evaly(ylhs,yrhs,yoverall)
        if better(score1,trivial,score):
          if yklass == num:
            if not greedy or ylhs.median()*trivial < yrhs.median(): 
              if goodxsplit(xlhs,xrhs,xoverall): # hook for stats
                cut,score = i+1,score1  
          else:
            if not greedy or ylhs.mode != yrhs.mode:
              if goodysplit(ylhs,yrhs,yoverall, score1):
                if goodxsplit(xlhs,xrhs,xoverall): # hook for stats
                  cut,score = i+1,score1
        #else:
         # print("nope")
    if verbose:
      score1 = round(score1,rnd) if score1 else '.'
      print(' ..'*lvl,xoverall.n,score1)
#      [print(' ++'*lvl,s) for s in segments]
    if cut:
      divide(segments[:cut], out= out, lvl= lvl+1)
      divide(segments[cut:], out= out, lvl= lvl+1)
    else:
      assert xoverall.lo <= xoverall.hi
      out.append(dict(label   = label, score = score,
                      x       = xoverall,
                      y       = yoverall,
                      has     = segments,id=len(out)))
    return out
  #------------------
  def chunks(l, n):
    for i in range(0, len(l), n):  yield l[i:i + n]
  #------------------
  if not lst:
    return []
  else:
    lst        = lst[:]
    yklass     = num if ynum else sym
    xall, yall = num(), yklass()
    width      = int(enough or len(lst)**enoughth)
    ordered    = sorted(lst,key=key)
    segments   = ordered if not flat else [z for z in chunks(ordered,width)]
    parts      = [stats(segment, xall, yall,flat) for segment in segments]
    epsilon    = epsilon or d * xall.wriggle()
    #[print(">>>",s) for s in segments]
    #print(dict(epsilon=epsilon,segs=segments))
    return divide(parts,out=[], lvl=0)
 
class ordered:
   def __init__(i,lst):
      i.sorted= False
      i._median = None
      i.all = lst
   def __add__(i,x):
      i.sorted=False
      i.all += [x]
   def wriggle(i):
     return i.median()
   def median(i):
     if not i.sorted or not i._median:
       i.sorted = True
       i.all    = sorted(i.all)
       n        = len(i.all)
       p  =  q  = n//2
       if n < 3:
         p,q = 0, n-1
       elif not n % 2:
         q = p -1
       i._median = i.all[p] if p==q else (i.all[p]+i.all[q])/2
     return i._median

class num:
    def __init__(i,inits=[]):
      i.lo, i.hi, i.n, i.mu, i.m2 = 1e32,-1e32,0,0,0
      i.sd = None
      i.all = []
      i.ordered=ordered(i.all)
      [i + x for x in inits]
    def __add__(i,x):
      i.ordered + x
      i.sorted=False
      i.lo   = min(x, i.lo)
      i.hi   = max(x, i.hi)
      i.n   += 1
      delta  = x - i.mu
      i.mu  += delta/i.n
      i.m2  += delta*(x - i.mu)
      if i.n > 1:
        i.sd = (i.m2/(i.n-1))**0.5
    def wriggle(i):
      return i.sd
    def median(i):
      return i.ordered.median()
    def __repr__(i):
      return "(:lo %.4f :hi %.4f :n %.4f :med %.4f :sd %.4f)" % (i.lo, i.hi, i.n,i.median(),i.sd)
   
class sym:
    def __init__(i,inits=[]):
      i.n, i.most, i.mode, i.counts = 0,0,None,{}
      i.all=[]
      i._ent=None
      [i + x for x in inits]
    def __add__(i,x):
      i.all += [x]
      i.n += 1
      i._ent=None
      count= i.counts[x] = i.counts.get(x,0) + 1
      if count > i.most:
        i.most,i.mode=count,x
    def wriggle(i): return i.ent()
    def ent(i):
      if i._ent is None:
        i._ent = 0
        for k in i.counts:
          p    = i.counts[k]/i.n
          i._ent -= p*math.log(p,2)
      return i._ent
    def k(i):  return len(i.counts.keys())
    def ke(i): return i.k()*i.ent()
    def __repr__(i):
      return 'n: %s most: %s more: %s ent: %s' % (i.n, i.most, i.more, i.ent()) 

```

