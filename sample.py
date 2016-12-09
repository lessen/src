from GLOBALS import our
from num     import num
from numbers import r
from cliffsDelta import cliffsDelta
from bootstrap   import bootstrap
import random

class sample:
  samples = our.sample.samples
  trivial = our.sample.trivial
  verbose = our.all.verbose
  cliffs  = our.sample.cliffs
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
    elif r() <= now/i.n:
      i.some[ int(r() * now) ]= x
  def ranges(i):
    return ranges(i.some)
  def bootstrap(i,j):
    return bootstrap(i.some,j.some,b=sample.b,conf=num.conf)
  def cliffsDelta(i,j):
    return cliffsDelta(i.some,j.some,sample.cliffs,sample.cliffs)


def leftRight(parts,epsilon=The.epsilon):
  """Iterator. For all items in 'parts',
  return everything to the left and everything
  from here to the end. For reasons of
  efficiency, take a first pass over the data
  to pre-compute and cache right-hand-sides
  """
  rights = {}
  n = j = len(parts) - 1
  while j > 0:
    rights[j] = parts[j]
    if j < n: rights[j] += rights[j+1]
    j -=1
  left = parts[0]
  for i,one in enumerate(parts):
    if i> 0:
      if parts[i]._median - parts[i-1]._median > epsilon:
        yield i,left,rights[i]
      left += one

def ranges(lst, x=same,y=same,enough=None,flat=True)
  
  def segments(lst):
    if flat:
      enough=enough
    if isinstance(x(lst[0]),(int,float)):
