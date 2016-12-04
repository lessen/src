class sym:
  def __init__(i,txt,col):
    i.name,i.col, i.counts = txt,col,{}
  def compile(i,x):
    return x
  def add(i,x):
    i.counts[x] = i.counts.get(x,0) + 1
    return x
  def dist(i,x,y,miss="?"):
    if   x == miss and y == miss : return 0,0
    elif x == miss or  y == miss : return 1,1
    else: return (0,1) if x==y else (1,1)
  def __repr__(i):
    return 'sym(%s,%s)' % (i.name,i.col)
        
