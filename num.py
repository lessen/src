from GLOBALS import our

class num:
  conf   = our.num.conf   # 95
  hedges = our.num.hedges # 0.38
  d      = our.num.d
  
  def __init__(i,inits=[]):
    i.lo, i.hi = 1e32,-1e32
    i.n, i.mu, i.m2 = 0,0,0
    map(i.add,inits)
  #-----------------
  # preparing
  def compile(i,x):
    return float(x)
  # -----------------
  # updating
  def add(i,x):
    i.lo = min(x, i.lo)
    i.hi = max(x, i.hi)
    i.n += 1
    delta = x - i.mu
    i.mu += delta/i.n
    i.m2 += delta*(x - i.mu)
  def sub(i,x):
    i.n  -= 1
    delta = x - i.mu
    i.mu  = max(0,i.mu - delta/i.n)
    i.m2  = max(0,i.m2 - delta*(x - i.mu))
  # --------------
  # distances
  def norm(i,x):
    x = (x - i.lo)/ (i.hi - i.lo + 1e-32)
    if x > 1: return 1
    if x < 0: return 0
    return x
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
  # -----------------------
  # stats
  def wriggle(i): return i.sd()
  def sd(i):
    return 0 if i.n <= 2 else (i.m2/(i.n-1))**0.5
  def hedgesTest(i,j):
    x   = (i.n - 1)*i.sd()**2 + (j.n - 1)*j.sd()**2
    y = (i.n - 1) + (j.n - 1)
    sp    = ( x / y )**0.5 + 1e-32
    delta = abs(i.mu - j.mu) / sp  
    c     = 1 - 3.0 / (4*(i.n + j.n - 2) - 1)
    return (delta * c) < num.hedges
  def ttest(i,j,
           criticals= {
                 95: {5:2.015, 10:1.812, 15:1.753,
                        20:1.725, 25:1.708, 30:1.697},
                 99: {5:3.365, 10:2.764, 15:2.602,
                        20:2.528, 25:2.485, 30:2.457}}):   
     df     = min(i.n - 1, j.n - 1)
     delta  = abs(i.mu - j.mu)
     si, sj = i.sd(), j.sd()
     tmp    = delta/((si/i.n + sj/j.n)**0.5) if si+sj else 1
     conf   = num.conf
     n1      = min(30,int(df/5 + 0.5)*5) # to fit into criticals
     return  tmp < criticals[num.conf][n1]
 

