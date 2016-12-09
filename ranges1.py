import math

from copy import deepcopy as copy

def expectedWriggle(lhs,rhs,all):
  return lhs.n()/all.n() * lhs.wriggle() + \
         rhs.n()/all.n() * rhs.wriggle()

def expectedMuChange(lhs,rhs,all):
  return lhs.n()/all.n() * abs(lhs.median() - all.median())**2 + \
         rhs.n()/all.n() * abs(rhs.median() - all.median())**2

def fayyadIranni(lhs,rhs,all,score):
  n     = all.n()
  gain  = all.ent() - score
  delta = math.log(3**all.k()-2,2) - (all.ke() - lhs.ke() - rhs.ke())
  return gain > (math.log(n-1,2) + delta)/n

def yes(*l,**d): return True

def ranges(lst,
           label      = "ranges",
           x          = lambda z:z,
           y          = lambda z:z,
           enough     = None,
           flat       = True,
           ynum       = True,
           enoughth   = 0.5,
           epsilon    = 0,
           d          = 0.3,
           trivial    = 1.01, # 1%
           evaly      = expectedWriggle,
           goodxsplit = yes
           goodysplit = yes):
  def stats(segment, xall, yall):
     x,y = num(),yklass()
     for z in x(segment):
       x    + z
       xall + z
     for z in y(segment):
       y   + z
       yall + z
     return x,y
  #-----------------
  def summary(segments):
    xs, ys, oldx, oldy = {}, {}, num(), yklass()
    for i,(x,y) in enumerate(segments[::-1]):
      j    = len(segments) - i - 1
      newx = copy(oldx)
      newy = copy(oldy)
      [newx + z for z in x.all]
      [newy + z for z in y.all]
      oldx= xs[j] = newx
      oldy= ys[j] = newy
    return xs, ys, copy(oldx), copy(oldy)
  #-----------------
  def divide(segments, out,lvl, cut=None):
    xrhsall, yrhsall, xoverall, yoverall = summary(segments)
    score, score1 = yoverall.wriggle(), None
    xlhs, ylhs    = num(), yklass()
    for i,(x,y) in enumerate(segments):
      xrhs = xrhsall[i]
      yrhs = yrhsall[i]
      [xlhs+z for z in x.all]
      [ylhs+z for z in y.all]
      if xlhs.lo - xoverall.lo > epsilon:
        if xoverall.hi - xlhs.hi > epsilon:
          score1 = evaly(ylhs,yrhs,yoverall)
          if score1*trivial < score:
            if yklass == num:
              if goodxsplit(xlhs,xrhs,xoverall): # hook for stats
                cut,score = i,score1  
            else:
              if goodysplit(ylhs,yrhs,yoverall, score1):
                if if goodxsplit(xlhs,xrhs,xoverall): # hook for stats
                  cut,score = i,score1
    if verbose:
      print('.. '*lvl,n,score1 or '.')
    if cut:
      divide(segments[:cut], out= out, lvl= lvl+1)
      divide(segments[cut:], out= out, lvl= lvl+1)
    else:
      out.append(dict(label = label, score = score,
                      start = xoverall.lo, stop  = xoverall.hi,
                      reportx = xoverall,
                      reporty = yoverall,
                      has     = segments,
                      n=xoverall.n,    id=len(out)))
    return out
  #------------------
  if not lst:
    return []
  else:
    segments = lst if not flat else [x for x in
                                     chunks(lst,
                                            enough or len(lst)**enoughth)]
    yklass     = num if ynum else sym
    xall, yall = num(), yklass()
    parts      = [stats(segment, xall, yall) for segment in segments]
    epsilon    = epsilon or d * xall.wriggle()
    parts      = sorted(parts,key=lambda z:z[0].median())
    return divide(parts,out=[], lvl=0)

class num:
    def __init__(i,inits=[]):
      i.lo, i.hi, i.n, i.mu, i.m2 = 1e32,-1e32,0,0,0
      i.sd = None
      i.ordered=ordered()
      [i + x for x in inits]
    def __add__(i,x):
      i.ordered + [x]
      i.sorted=False
      i.lo  = min(x, i.lo)
      i.hi  = max(x, i.hi)
      i.n  += 1
      delta = x - i.mu
      i.mu += delta/i.n
      i.m2 += delta*(x - i.mu)
      if i.n > 1:
        i.sd = (i.m2/(i.n-1))**0.5
    def wriggle(i):
      return i.sd
    def median(i):
      return i.ordered.median()

class ordered:
    def __init__(i):
      i.sorted= False
      i._median = None
      i.all = []
   def __add__(i,x):
      i.sorted=False
      i.all += [x]
   def wriggle(i):
     return i.median()
   def median(i):
     if not i.sorted or not i._median:
       i.sorted = True
       i.all    = sorted(i.all)
       n        = len(i.median)
       p  =  q  = n//2
       if n < 3:
         p,q = 0, n-1
       elif not n % 2:
         q = p -1
       i._median = (i.all[p]+i.all[q])/2
     return i._median

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
        for val in i.counts.values():
          p    = val/i.n
          i._ent -= p*math.log(p,2)
      return i._ent
    def k(i):  return len(i.counts.keys())
    def ke(i): return i.k()*i.ent()

def chunks(l, n):
  for i in range(0, len(l), n): yield l[i:i + n]    
