import math

class sym:
  def __init__(i,txt,col):
    i.n, i.most, i.mode = 0,0,None
    i.name,i.col, i.counts = txt,col,{}
  
  # ----------------
  # preparing
  def compile(i,x):
    return x
  # ----------
  # updating
  def add(i,x):
    i.n += 1
    count= i.counts[x] = i.counts.get(x,0) + 1
    if count > i.most:
      i.most,i.mode=count,x
  def sub(i,x):
    i.n   = max(0,i.n - 1)
    i.counts[x] = max(0, i.counts[x] - 1)
    if x == i.mode:
      i.most, i.mode = None,None
  # ---------
  # distance
  def dist(i,x,y,miss="?"):
    if   x == miss and y == miss : return None
    elif x == miss or  y == miss : return 1
    else: return 0 if x==y else 1
  # --------
  # stats
  def like(i,x,prior=0,m=0):
     return (i.counts.get(x,0) + m*prior)/(i.n + m)
  def k(i):
    return len(i.counts.keys())
  def ent(i):
    tmp = 0
    for val in i.counts.values():
      p = val/i.n
      if p:
        tmp -= p*math.log(p,2)
    return tmp 
  # ---------------
  # reporting
  def __repr__(i):
    return 'sym(%s,%s)' % (i.name,i.col)
