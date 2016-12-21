import math

class sym:
  def __init__(i):
    i.n, i.most, i.mode, i.counts = 0,0,None,{}
    i._ent=None
  def add(i,x):
    i._ent=None
    i.n += 1
    count= i.counts[x] = i.counts.get(x,0) + 1
    if count > i.most:
      i.most,i.mode=count,x
  def dist(i,x,y,miss="?"):
    if   x == miss and y == miss : return None
    elif x == miss or  y == miss : return 1
    else: return 0 if x==y else 1
  def like(i,x,prior=0,m=0):
     return (i.counts.get(x,0) + m*prior)/(i.n + m)
  def __repr__(i):
    return 'sym(%s,%s)' % (i.name,i.col)
