class num:
  HEDGES = our.num.hedges # 0.38
  CONF   = our.num.conf   # 0.95
  def __init__(i,txt,col):
    i.name, i.col, i.lo, i.hi = txt,col,1e32,-1e32
    i.n, i.mu, i.m2 = 0,0,0
  def compile(i,x):
    return float(x)
  def add(i,x):
    i.lo = min(x, i.lo)
    i.hi = max(x, i.hi)
    i.n += 1
    delta = x - i.mu
    i.mu += delta/i.n
    i.m2 += delta*(x - i.mu)
    return x
  def sub(i,x):
    i.n   = max(0,i.n - 1)
    delta = x - i.mu
    i.mu  = max(0,i.mu - delta/i.n)
    i.m2  = max(0,i.m2 - delta*(x - i.mu))
  def sd(i):
    return 0 if i.n <= 2 else (i.m2/(i.n-1))**0.5
  def norm(i,x):
    x = (x - i.lo) / (i.hi - i.lo + 1e-32)
    if x > 1: return 1
    if x < 0: return 0
    return x
  def dist(i,x,y,miss="?"):
    if x == miss and y == miss: return 0,0
    if x == miss:
      y = i.norm(y)
      x = 1 if i.norm(y) < 0.5 else 0
    elif y == miss:
      x = i.norm(x)
      y = 1 if i.norm(x) < 0.5 else 0
    else:
      x,y = i.norm(x), i.norm(y)
    return (x-y)**2, 1  
  def __repr__(i):
    return 'num(%s,%s)' % (i.name,i.col)
  def smallEffect(i,j):
    small = num.HEDGES
    num   = (i.n - 1)*i.s**2 + (j.n - 1)*j.s**2
    denom = (i.n - 1) + (j.n - 1)
    sp    = ( num / denom )**0.5
    delta = abs(i.mu - j.mu) / sp  
    c     = 1 - 3.0 / (4*(i.n + j.n - 2) - 1)
    return delta * c < small
  def same(i,j,
          nums= {0.95: {5:2.015, 10:1.812, 15:1.753,
                        20:1.725, 25:1.708, 30:1.697}
                 0.99: {5:3.365, 10:2.764, 15:2.602,
                        20:2.528, 25:2.485, 30:2.457}}):   
     df     = min(i.n - 1, j.n - 1)
     n      = min(30,int(df/5 + 0.5)*5)
     delta  = abs(i.mu - j.mu)
     si, sj = i.sd(), j.sd()
     tmp    = delta/((si/i.n + sj/j.n)**0.5) if si+sj else 1
     return  tmp > nums[conf][n]
  def different(i,j):
    return i.smallEffort(j) or i.same(j)

