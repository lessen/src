"""
Returns true if two lists are not statistically significantly different.

Based on [An introduction to the
bootstrap](https://github.com/timm/timm.github.io/blob/master/pdf/93bootstrap.pdf)
by Bradley Efron, 1993, Chapman and Hall, page 220 to 224.


Works via `bootstrap sampling`:


- On the original two lists, determine some difference between the lists
  (this is computed via a `testStatistic` function).
- Check if that difference is "stable" across multiple samples of
  the data. 
     - Count how many times we can see a diffferent and bigger difference
       in the sampled lists (again, computed via `testStatistic`, but
       this time on the sampled data).
     - If that count is _rare_ (as defined by the `conf` value,
       then return `True`.
 

____

## Programmer's Guide

"""
import random
  
def bootstrap(y0,z0, b = 1000, conf= 95):
  tiny=1e-32 # added to some divisions to stop div zero errors

  # ### Helpers

  # Return any number 0 to n
  def any(n): return random.uniform(0,n)

  # Return any list item (uses `any`).
  def one(lst): return lst[ int(any(len(lst))) ]
  
  # Return any sample from `lst` (uses `one`).
  def sampleWithReplacement(lst):
    return [one(lst) for _ in lst]
  
  # The test statistic: comments on the difference between two lists
  def testStatistic(y,z): 
    tmp1 = tmp2 = 0
    for y1 in y.all: tmp1 += (y1 - y.mu)**2 
    for z1 in z.all: tmp2 += (z1 - z.mu)**2
    s1    = (tmp1 / (y.n - 1 + tiny))**0.5
    s2    = (tmp2 / (z.n - 1 + tiny))**0.5
    delta = abs(z.mu - y.mu)
    if s1+s2:
      delta =  delta/((s1/(y.n + tiny) + s2/(z.n + tiny))**0.5)
    return delta
  
  #______
  # ### Num class
  
  # A counter class to simplify reasoning about sets of numbers
  class num():
    def __init__(i,some=[]):
      i.sum = i.n = i.mu = 0 ; i.all=[]
      for one in some:
        i.put(one)
    def put(i,x):
      i.all.append(x);
      i.sum +=x; i.n += 1
      i.mu   = i.sum/(i.n + tiny)
    def __add__(i1,i2):
      return num(i1.all + i2.all)
    
 
  # -------------------------
  # ### Run this script
  
  # Some set up
  y, z   = num(y0), num(z0)
  x      = y + z
  tobs   = testStatistic(y,z)

  # Effron recommends adjusting all the populations so they have the same mean
  yhat   = [y1 - y.mu + x.mu for y1 in y.all]
  zhat   = [z1 - z.mu + x.mu for z1 in z.all]
  
  # Count how often we see a diffferent and bigger difference
  # in the sampled lists
  bigger = tiny
  for i in range(b):
    if testStatistic(num(sampleWithReplacement(yhat)),
                     num(sampleWithReplacement(zhat))) > tobs:
      bigger += 1

  # Return true if we "rarely" see these different and bigger differences
  # (and "rarely" is defined by `conf`).
  return (bigger / b) > (1 - conf/100)

