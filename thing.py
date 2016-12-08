import random
from   misc    import same
from GLOBALS import our
from num     import num
from sym     import sym
from numbers import r
from sample  import sample

def things(xs):
  xs= xs if isinstance(xs,(list,tuple)) else [xs]
  for x in xs:
    if x != thing.unknown:
      yield x

class thing:
  unknown = our.thing.unknown
  
  def __init__(i,inits=[],pos=None, txt=None,samples=None):
    txt = txt or pos
    i.txt=str(txt)
    i.pos=pos
    i.want,i.my=None,None
    i.samples=sample()
    i.add(inits)
  def add(i,xs):
    for x in things(xs):
      if i.my is None:
        what = num if isinstance(x,(float,int)) else sym
        i.my  = what()
      i.my.add(x)
      i.samples.add(x)
  def sub(i,xs):
    assert i.my != None
    for x in things(xs):
      if i.my.n > 1:
        i.my.sub(x)
  def n(i):
    return i.my.n
  
  #--- non-parametric tests, defined in samples
  def cliffsDelta(i,j): return i.samples.cliffsDelta(j.samples)
  def ranges(i)       : return i.samples.ranges()
  def bootstrap(i,j)  : return i.samples.bootstrap(j.samples)
  def same_CD(i,j)    : return i.cliffsDelta(j) and i.bootstrap(j)
  
  #--- generic. returns sd for nums and entropy for syms
  def wriggle(i)      : return i.my.wriggle()

  #--- parametric. assumes gaussians
  def same_HT(i,j)    : return i.hedgesTest(j) and i.ttest(j)
  def ttest(i,j)      : return i.my.ttest(j.my)
  def hedgesTest(i,j) : return i.my.hedgesTest(j.my)

  # -- pretty print
  def __repr__(i):
    return 'thing(%s,%s)' % (i.txt,i.pos)


