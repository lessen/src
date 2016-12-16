import sys,math
from copy import deepcopy as copy

def expectedWriggle(lhs,rhs,all):
  #print(dict(nlhs=lhs.n,
   #          wlhs=lhs.wriggle(),
    #         nrhs=rhs.n,
     #        wrhs=rhs.wriggle(),
      #       nall=all.n,
       #      wall=all.wriggle()
        #     ))
  tmp = lhs.n/all.n * lhs.wriggle() + \
         rhs.n/all.n * rhs.wriggle()
  #print(tmp)
  return tmp

def expectedMuChange(lhs,rhs,all):
  return lhs.n/all.n * abs(lhs.median() - all.median())**2 + \
         rhs.n/all.n * abs(rhs.median() - all.median())**2

def fayyadIranni(lhs,rhs,all,score):
  gain  = all.ent() - score
  delta = math.log(3**all.k()-2,2) - (all.ke() - lhs.ke() - rhs.ke())
  return gain > (math.log(all.n-1,2) + delta)/all.n

def yes(*l,**d): return True

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
     return "(:lo %s :hi %s :n %s)" % (i.lo, i.hi, i.n)
   
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
    
#-----------------------------------
def ranges(lst,
           d          = 0.3,
           enough     = None,
           enoughth   = 0.5,
           epsilon    = 0,
           evaly      = expectedWriggle,
           flat       = True,
           goodxsplit = yes,
           goodysplit = yes,
           label      = "ranges",
           rnd        = 3,
           trivial    = 1.01, # 1%
           key        = lambda z:z,
           verbose    = False,
           x          = lambda z:z,
           y          = lambda z:z,
           ynum       = True,
          ):
  def stats(segment, xall, yall,flat):
     xs,ys = num(),yklass()
     for one in segment:
       x1=x(one)
       y1=y(one)
       xs   + x1
       xall + x1
       ys   + y1
       yall + y1
     return xs,ys
  #-----------------
  def summary(segments):
    xall,yall=[],[]
    xs, ys, oldx, oldy = {}, {}, num(), yklass()
    for i,(x,y) in enumerate(segments[::-1]):
      j    = len(segments) - i - 1
      xall += x.all
      yall += y.all
      newx = num(xall)
      newy = yklass(yall)
      [newx + z for z in x.all]
      [newy + z for z in y.all]
      oldx= xs[j] = newx
      oldy= ys[j] = newy
    return xs, ys, num(xall), yklass(yall)
  #-----------------
  def divide(segments, out,lvl, cut=None):
    xrhsall, yrhsall, xoverall, yoverall = summary(segments)
    
    score, score1 = yoverall.wriggle(), None
    xlhs, ylhs    = num(), yklass()
    for i,(x,y) in enumerate(segments[:-2]):
      xrhs = xrhsall[i+1]
      yrhs = yrhsall[i+1]
      [xlhs+z for z in x.all]
      [ylhs+z for z in y.all]
      if   xoverall.lo < xlhs.median() - epsilon:
        if xoverall.hi > xlhs.median() + epsilon :
          score1 = evaly(ylhs,yrhs,yoverall)
          if score1*trivial < score:
            if yklass == num:
              if goodxsplit(xlhs,xrhs,xoverall): # hook for stats
                cut,score = i+1,score1  
            else:
              if goodysplit(ylhs,yrhs,yoverall, score1):
                if goodxsplit(xlhs,xrhs,xoverall): # hook for stats
                  cut,score = i+1,score1
    if verbose:
      score1 = round(score1,rnd) if score1 else '.'
      print(' ..'*lvl,xoverall.n,score1)
    if cut:
      divide(segments[:cut], out= out, lvl= lvl+1)
      divide(segments[cut:], out= out, lvl= lvl+1)
    else:
      assert xoverall.lo < xoverall.hi
      out.append(dict(label   = label, score = score,
                      start   = xoverall.lo, stop  = xoverall.hi,
                      reportx = xoverall,
                      reporty = yoverall,
                      has     = segments,
                      n=xoverall.n,    id=len(out)))
    return out
  #------------------
  def chunks(l, n):
    for i in range(0, len(l), n):  yield l[i:i + n]
  #------------------
  if not lst:
    return []
  else:
    yklass     = num if ynum else sym
    xall, yall = num(), yklass()
    width      = int(enough or len(lst)**enoughth)
    ordered    = sorted(lst,key=key)
    segments   = ordered if not flat else [z for z in chunks(ordered,width)]
    
    parts      = [stats(segment, xall, yall,flat) for segment in segments]
    
    epsilon    = epsilon or d * xall.wriggle()
    return divide(parts,out=[], lvl=0)

