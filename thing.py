import random
from GLOBALS import our
from num import num
from sym import sym
from numbers import r

class thing:
  unknown = our.thing.unknown
  samples = our.thing.samples
  cliffs = our.thing.cliffs # 0.56
  b = our.thing.b
  trival=our.thing.trival
  verbose = our.thing.verbose
  
  def __init__(i,inits=[],pos=None, txt=None,samples=None):
    txt = txt or pos
    i.txt=str(txt)
    i.pos=pos
    i.some=[]
    i.n  = 0
    i.max= samples or thing.samples
    i.want,i.my=None,None
    i.ordered=False
    i.add(inits)
  def add(i,xs):
    for x in things(xs):
      if i.my is None:
        what = num if isinstance(x,(float,int)) else sym
        i.my  = what()
      i.my.add(x)
      i.addSome(x)
  def addSome(i,x):
    i.ordered=False
    i.n += 1
    now  = len(i.some)
    if now < i.max:
      i.some.append(x)
    elif r() <= now/i.n:
      i.some[ int(r() * now) ]= x
  def sub(i,xs):
    assert i.my != None
    for x in things(xs):
      if i.my.n > 1:
        i.my.sub(x)
  def wriggle(i)     : return i.my.wriggle() 
  def same(i,j)      : return i.my.same(j.my)
  def sureSame(i,j)  : return i.cliffsDelta(j) and i.bootstrap(j)
  def ttest(i,j)     : return i.my.ttest(j.my)
  def hedgesTest(i,j): return i.my.hedgesTest(j.my)
  def bootstrap(i,j) : return bootstrap(i.some, j.some)
  
  def cliffsDelta(i,j):
    lt=gt=n=0
    for x in i.some:
      for y in j.some:
        n += 1
        if x > y: gt +=1
        if x < y: lt +=1
    return abs(gt-lt)/n < thing.cliffs
  def __repr__(i):
    return 'thing(%s,%s)' % (i.txt,i.pos)

def things(xs):
  xs= xs if isinstance(xs,(list,tuple)) else [xs]
  for x in xs:
    if x != thing.unknown:
      yield x

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
  for i in range(thing.b):
    if testStatistic(total(sampleWithReplacement(yhat)),
                     total(sampleWithReplacement(zhat))) > tobs:
      bigger += 1
  return (bigger / thing.b) > (1 - num.conf/100)

def expectedWriggle(lhs,rhs,all):
  return lhs.n/all.n * rhs.wriggle() + \
         rhs.n/all.n * rhs.wriggle()

def expectedMuChange(lhs,rhs,all):
  return lhs.n/all.n * abs(lhs.mu - all.mu)**2 + \
         rhs.n/all.n * abs(rhs.mu - all.mu)**2

def div(lst,label=0, x= same, y= same, order=None,f=expectedWriggle):
  def divide(lst, out=[], lvl=0, cut=None):  
    xlhs, xrhs   = thing(),        thing(map(x,lst))
    ylhs, yrhs   = thing(),        thing(map(y,lst))
    score,score1 = yrhs.wriggle(), None
    n            = xrhs.n
    overall       = thing(map(y,lst))
    start,stop   = x.my.lo, x.my.hi
    for i,new in enumerate(lst):
        here =  x(new)
        there=  y(new)
        xlhs.add(here) ; xrhs.sub(here)
        ylhs.add(there); yrhs.sub(there)
        if xrhs.n >= enough:
          if xlhs.n >= enough:
            if here - start > tiny:
              if stop - here > tiny:
                score1 = f(lhs,rhs,overall)
                if score1*thing.trivial < score:
                  if isinstance(yrhs.my,num):
                    cut,score= i,score1
                  else:
                    k0,e0,ke0 = yrhs.my.k(), yrhs.my.ent()
                    ke0       = k0*e0
                    gain      = e0 - score1
                    delta     = math.log(3**k0-2,2)-(ke0- yrhs.my.ke() - ylhs.my.ke())#bug here?
                    border    = (math.log(n-1,2) + delta)/n
                    if gain >= border:
                      cut,score = i,score1
    if thing.verbose:
      print('.. '*lvl,len(lst),score1 or '.')
    if cut:
      divide(lst[:cut], out= out, lvl= lvl+1)
      divide(lst[cut:], out= out, lvl= lvl+1)
    else:
      out.append(dict(label=label, score=score, report=overall,
                       n=n,  id=len(out),
                       lo=start, up=stop,
                       has=lst))
    return out
    # --- end function divide -----------------------------
  if not lst: return []
  tiny   = thing.d * thing(map(x,lst)).wriggle() 
  enough = len(lst)**thing.enough
  order  = order  or x
  return divide( sorted(lst[:], key=order), out=[] ,lvl=0) # copied, sorted
