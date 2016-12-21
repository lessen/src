""" 
Maintains summaries of numbers. Can be used incrementally, or in batch.

Example of incremental usage:

        n=num()
        for i in range(1000):
          n + i
          if i % 100 == 0: print(n)

        # output:
        {:n 1 :lo 0 :hi 0 :mu 0 :sd 0}
        {:n 101 :lo 0 :hi 100 :mu 50 :sd 29.3}
        {:n 201 :lo 0 :hi 200 :mu 100 :sd 58.17}
        {:n 301 :lo 0 :hi 300 :mu 150 :sd 87.04}
        {:n 401 :lo 0 :hi 400 :mu 200 :sd 115.9}
        {:n 501 :lo 0 :hi 500 :mu 250 :sd 144.8}  
        {:n 601 :lo 0 :hi 600 :mu 300 :sd 173.6}
        {:n 701 :lo 0 :hi 700 :mu 350 :sd 202.5}
        {:n 801 :lo 0 :hi 800 :mu 400 :sd 231.4}
        {:n 901 :lo 0 :hi 900 :mu 450 :sd 260.2}

Example of batch usage:

      print(num(i for i in range(901)))

      # output:
      {:n 901 :lo 0 :hi 900 :mu 450 :sd 260.2}

Also, can be used to:

- compute distance between numbers (used in nearest-neighbor calculations);
- compute likelihood a number belongs to a sample (used in Bayes classifiers);
- compute parametric tests for effect size and statistical hypothesis checking

_____________________
## Programmer's guide        
"""

from math import pi,e

class num:
  
  # Initialization
  def __init__(i,inits=[]):
    i.lo, i.hi = 1e32,-1e32
    i.n, i.mu, i.m2 = 0,0,0
    [i + x for x in inits]
  # Reporting
  def __repr__(i):
    return "{:n %s :lo %s :hi %s :mu %g :sd %.4g}" % (i.n, i.lo, i.hi, i.mu, i.sd())
  
  # Updating (uses Knuth's method to also update `sd`-related info).
  def __add__(i,x):
    i.lo  = min(x, i.lo)
    i.hi  = max(x, i.hi)
    i.n  += 1
    delta = x - i.mu
    i.mu += delta/i.n
    i.m2 += delta*(x - i.mu)
    
  # Calculate sd using Knuth's method.
  def sd(i):
    return 0 if i.n <= 2 else (i.m2/(i.n-1))**0.5
  #----------------------------------------------------------------------------
  # ### Distance calculations
  
  # Distance between two numbers, defined as per p42 of [Aha et al., 1991](https://goo.gl/2722eJ):
  #
  # - numerics are normalized zero to one
  # - when faced with unknown values, assume maximal distance.
  def dist(i,x,y,miss="?"):
    if x == miss and y == miss: return None
    if x == miss:
      y = i.norm(y)
      x = 1 if i.norm(y) < 0.5 else 0 
    elif y == miss:
      x = i.norm(x)
      y = 1 if i.norm(x) < 0.5 else 0
    else:
      x,y = i.norm(x), i.norm(y)
    return (x-y)**2
  # Normalization. Adds a tiny amount to the denominator to stop divide by zero errors.
  def norm(i,x):
    return max(0, min(1, (x - i.lo)/ (i.hi - i.lo + 1e-32)))
  
  # Calculates how likely is it that number `x` belongs to this distribution (used in Bayes classifiers).
  def like(i,x,*_): # ignored third argument is needed to match usage of `like` in `sym`.
    var   = i.sd()**2
    denom = (2*pi*var)**.5
    num   = e**(-(x-i.mu)**2/(2*var))
    return num/denom
  # ---------------------------------------------------------
  # ### Statistics
  
  # Two distributions are different if they are not statistically
  # significantly similar and if they are not different by just a small
  # effect size.
  def diff(i,j):
    return not i.hedges(j) and not i.ttest(j)
    
  # Parametric effect size test (uses eqns 1,2,3,4 and Table9 from 
  # [Kampenes et al., 2007](https://goo.gl/WBDWm3)).
  def hedges(i,j,enough = 0.38):
    x   = (i.n - 1)*i.sd()**2 + (j.n - 1)*j.sd()**2
    y = (i.n - 1) + (j.n - 1)
    sp    = ( x / y )**0.5 + 1e-32
    delta = abs(i.mu - j.mu) / sp  
    c     = 1 - 3.0 / (4*(i.n + j.n - 2) - 1)
    return (delta * c) < enough
  
  # Parametric statistical signifance test (the standard t-test).
  def ttest(i,j, conf=95,
           criticals= { # approximations to the table of critical values
                   95: {  5:2.015, 10:1.812, 15:1.753,
                         20:1.725, 25:1.708, 30:1.697},
                   99: {  5:3.365, 10:2.764, 15:2.602,
                         20:2.528, 25:2.485, 30:2.457}}):   
     df     = min(i.n - 1, j.n - 1)
     delta  = abs(i.mu - j.mu)
     si, sj = i.sd(), j.sd()
     tmp    = delta/((si/i.n + sj/j.n)**0.5) if si+sj else 1
     n1     = min(30,int(df/5 + 0.5)*5) # to fit into criticals
     return  tmp < criticals[conf][n1]
