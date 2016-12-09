import random,math

####################################################

def expectedWriggle(lhs,rhs,all):
  return lhs.n()/all.n() * rhs.wriggle() + \
         rhs.n()/all.n() * rhs.wriggle()

def expectedMuChange(lhs,rhs,all):
  return lhs.n()/all.n() * abs(lhs.my.mu - all.my.mu)**2 + \
         rhs.n()/all.n() * abs(rhs.my.mu - all.my.mu)**2

def yes(*l): return True

class num:
  def __init__(i,inits=[]):
    i.lo, i.hi, i.n, i.mu, i.m2,i.sd = 1e32,-1e32,0,0,0,0
    [i.add(x) for x in inits]
  def add(i,x):
    i.lo  = min(x, i.lo)
    i.hi  = max(x, i.hi)
    i.n  += 1
    delta = x - i.mu
    i.mu += delta/i.n
    i.m2 += delta*(x - i.mu)
    if i.n > 1:
      i.sd = (i.m2/(i.n-1))**0.5
  def wriggle(i): return i.sd

class sym:
  def __init__(i):
    i.n, i.most, i.mode, i.counts = 0,0,None,{}
    i.ent=None
  def add(i,x):
    i.ent=None
    i.n += 1
    count= i.counts[x] = i.counts.get(x,0) + 1
    if count > i.most:
      i.most,i.mode=count,x
  def wriggle(i):
    if i.ent is None:
      tmp = 0
      for val in i.counts.values():
        p    = val/i.n
        tmp -= p*math.log(p,2)
      i.ent = tmp
    return i.ent
  def k(i):  return len(i.counts.keys())
  def ke(i): return i.k()*i.ent()

  
# XXX the rhs will need to be calced
def ranges(lst,label=0,
        x       = lambda z1:z1,
        y       = lambda z2:z2,
        same    = lambda z3,z4: False,
        order   = None,
        enough  = None,
        epsilon = None,
        scoring = expectedWriggle
       ):
  def divide(lst, out=[], lvl=0, cut=None):
    xs           = [x(z) for z in lst]
    ys           = [y(z) for z in lst]
    overally     = thing(ys)
    overallx     = thing(xs)
    score,score1 = overally.wriggle(), None
    start,stop   = overallx.my.lo, overallx.my.hi
    n            = overallx.n()
    #if n >= enough:
    xlhs, xrhs   = thing(), thing(xs)
    ylhs, yrhs   = thing(), thing(ys)
    e0,k0        = None, None
    for i,new in enumerate(lst):
      here =  x(new)
      there =  y(new)
      xrhs.sub(here)  ; xlhs.add(here)  
      yrhs.sub(there) ; ylhs.add(there)
      if isinstance(here,list): startHere,stopHere = here[0], here[-1]
      else                    : startHere,stopHere = here, here
      if xrhs.n() >= enough:
        if xlhs.n() >= enough:
          #print(".")
          if startHere - start > epsilon:
            if stop - stopHere > epsilon:
              score1 = scoring(ylhs,yrhs,overally)
              if score1*sample.trivial < score:
                if isinstance(yrhs.my,num):
                  if not same(lst,xlhs,ylhs,i,x,y):
                    cut,score= i,score1
                else:
                  e0     = e0 or overally.my.ent()
                  k0     = k0 or overally.my.k()
                  ke0    = e0*ke0
                  gain   = e0 - score1
                  delta  = math.log(3**k0-2,2)- (ke0 - yrhs.my.ke() - ylhs.my.ke())
                  border = (math.log(n-1,2) + delta)/n
                  if gain >= border:
                    if not same(lst,xlhs,ylhs,i,x,y):
                      cut,score = i,score1
    if sample.verbose:
      print('.. '*lvl,n,score1 or '.')
    if cut:
      divide(lst[:cut], out= out, lvl= lvl+1)
      divide(lst[cut:], out= out, lvl= lvl+1)
    else:
      out.append(dict(label=label, score=score, report=overallx,
                       n=n,  id=len(out),
                       lo=start, up=stop, #has=lst
                       ))
    return out
    # --- end function divide -----------------------------
  if not lst: return []
  epsilon   = epsilon   or num.d * thing([x(z) for z in lst]).wriggle() 
  enough = enough or len(lst)**sample.enough
  order  = order  or x
  return divide( sorted(lst[:], key=order), out=[] ,lvl=0) # copied, sorted

