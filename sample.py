
from GLOBALS import our
from num     import num
from numbers import r
import random

class sample:
  samples=our.sample.samples
  trivial=our.sample.trivial
  verbose=our.all.verbose
  cliffs=our.sample.cliffs
  b       = our.sample.b
  enough  = our.sample.enough

  def __init__(i,inits=[],samples=None):
    i.max = samples or sample.samples
    i.some,i.n= [],0
    i.ordered=False
    [i.add(x) for x in inits]
  def add(i,x):
    i.ordered=False
    i.n += 1
    now  = len(i.some)
    if now < i.max:
      i.some.append(x)
    elif r() <= now/i._n:
      i.some[ int(r() * now) ]= x
  def ranges(i):
    return ranges(i.some)
  def bootstrap(i,j):
    return bootstrap(i.some,j.some)
  def cliffsDelta(i,j):
    lt=gt=n=0
    for x in i.some:
      for y in j.some:
        n += 1
        if x > y: gt +=1
        if x < y: lt +=1
    return abs(gt-lt)/n < sample.cliffs

#########################################
  
def bootstrap(y0,z0):
  "From p220 to 223 of Efron's book 'An introduction to the boostrap."
  def testStatistic(y,z): 
    tmp1 = tmp2 = 0
    for y1 in y.all: tmp1 += (y1 - y.mu)**2 
    for z1 in z.all: tmp2 += (z1 - z.mu)**2
    s1    = (float(tmp1)/(y.n - 1))**0.5
    s2    = (float(tmp2)/(z.n - 1))**0.5
    delta = abs(z.mu - y.mu)
    if s1+s2:
      delta =  delta/((s1/y.n + s2/z.n)**0.5)
    return delta
  # -------------------------
  class total():
    def __init__(i,some=[]):
      i.sum = i.n = i.mu = 0 ; i.all=[]
      for one in some: i.put(one)
    def put(i,x):
      i.all.append(x);
      i.sum +=x; i.n += 1; i.mu = float(i.sum)/i.n
    def __add__(i1,i2): return total(i1.all + i2.all)
  # -------------------------
  def sampleWithReplacement(lst):
    def any(n)  : return random.uniform(0,n)
    def one(lst): return lst[ int(any(len(lst))) ]
    return [one(lst) for _ in lst]
  # -------------------------
  y, z   = total(y0), total(z0)
  x      = y + z
  tobs   = testStatistic(y,z)
  yhat   = [y1 - y.mu + x.mu for y1 in y.all]
  zhat   = [z1 - z.mu + x.mu for z1 in z.all]
  bigger = 0.0
  for i in range(sample.b):
    if testStatistic(total(sampleWithReplacement(yhat)),
                     total(sampleWithReplacement(zhat))) > tobs:
      bigger += 1
  return (bigger / sample.b) > (1 - num.conf/100)

####################################################

def expectedWriggle(lhs,rhs,all):
  return lhs.my.n/all.my.n * rhs.wriggle() + \
         rhs.my.n/all.my.n * rhs.wriggle()

def expectedMuChange(lhs,rhs,all):
  return lhs.my.n/all.my.n * abs(lhs.my.mu - all.my.mu)**2 + \
         rhs.my.n/all.my.n * abs(rhs.my.mu - all.my.mu)**2

def yes(*l): return True

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
    n            = overallx.my.n
    if n >= enough:
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
        if xrhs.my.n >= enough:
          if xlhs.my.n >= enough:
            #print(".")
            if startHere - start > epsilon:
              if stop - stopHere > epsilon:
                score1 = scoring(ylhs,yrhs,overally)
                if score1*sample.trivial < score:
                  if not same(ylhs,yrhs):
                    if isinstance(yrhs.my,num):
                      cut,score= i,score1
                    else:
                      e0     = e0 or overally.my.ent()
                      k0     = k0 or overally.my.k()
                      ke0    = e0*ke0
                      gain   = e0 - score1
                      delta  = math.log(3**k0-2,2)- (ke0 - yrhs.my.ke() - ylhs.my.ke())
                      border = (math.log(n-1,2) + delta)/n
                      if gain >= border:
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
  enough = enough or len(lst)**thing.enough
  order  = order  or x
  return divide( sorted(lst[:], key=order), out=[] ,lvl=0) # copied, sorted
