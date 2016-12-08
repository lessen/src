from GLOBALS import our
from num import num
from sym import sym
from numbers import r

class thing:
  unknown = our.thing.unknown
  samples = our.thing.samples
  cliffs = our.thing.cliffs # 0.56
  
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
    for x in items(xs):
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
    for x in items(xs):
      if i.my.n > 1:
        i.my.sub(x)
  def same(i,j)      : return i.my.same(j.my)
  def ttest(i,j)     : return i.my.ttest(j.my)
  def hedgesTest(i,j): return i.my.hedgesTest(j.my)
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

def items(xs):
  xs= xs if isinstance(xs,(list,tuple)) else [xs]
  for x in xs:
    if x != thing.unknown:
      yield x
