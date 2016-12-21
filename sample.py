from GLOBALS import our
from num     import num
from random import random as r
from cliffsDelta import cd
from bootstrap   import bootstrap

class sample:
  SAMPLES = 256
  trivial = our.sample.trivial
  verbose = our.all.verbose
  cliffs  = our.sample.cliffs
  b       = our.sample.b
  enough  = our.sample.enough

  def __init__(i,inits=[],samples=None):
    i.max = samples or sample.SAMPLES
    i.some,i.n= [],0
    i.ordered=False
    [i.add(x) for x in inits]
  def add(i,x):
    i.ordered=False
    i.n += 1
    now  = len(i.some)
    if now < i.max:
      i.some.append(x)
    elif r() <= now/i.n:
      i.some[ int(r() * now) ]= x
  def ranges(i):
    return ranges(i.some)
  def bootstrap(i,j,b=1000,conf=95):
    return bootstrap(i.some,j.some,b=b,conf=conf)
  def cliffsDelta(i,j,trivial):
    return cd(i.some,j.some, trivial=trivial)

