from num import num
import remedian
import cliffsDelta

def same(lst1,lst2):
  return not cliffsDelta.cliffsDelta(lst1,lst2,0.147)

class seens:
  def __init__(i,objs,inits=[]):
    i.all=None
    i.objs=objs
    [i+x for x in inits]
  def clone(i,inits=[]):
    return seens(i.objs,inits)
  def __add__(i,x):
    ys = i.objs(x)
    if y.all is None:
      i.all = [seen(pos) for pos,_ in enumerate(ys)]
    [see + y for see,y in zip(i.all,ys)]
  def same(i,j, f = same):
    for x,y in zip(i.all, j.all):
      if not f(x,y):
        return False
    return True

# need a post-prune
class seen:
  def __init__(i,pos=None,inits=[]):
    i.pos = pos
    i.med = remedian.remedian()
    i.n, i.mu, i.m2, i.sd, i.all = 0,0,0,0,[]
    [i + x for x in inits]
  def __add__(i):
    i.med + x
    i.all += [x]
    i.n  += 1
    delta = x - i.mu
    i.mu += delta/i.n
    i.m2 += delta*(x - i.mu)
    if i.n > 2:
      i.sd = (i.m2/(i.n-1))**0.5
  def __lt__(i,j):
    return i.sd > j.sd # so higest var goes first

def clusters(lst,objs,s=None,p=0.25, ame= same)
  s = s or len(lst)**p)
  return prune(
            tree(lst,objects,s,f),
            same)

def leaf(t): 
  return t.left == t.right == None

def prune(t, ne):
  if t.left and t.right and leaf(t.left) and leaf(t.right)
    if different(t.left,r.right,ne):
      t.left= t.right= None
  elif t.left and not t.right and leaf(t.left):
    if different(t.all,t.left,ne):
      t.left = None
  elif t.right and not t.left and leaf(t.right):
    if different(t.all,t.right,ne):
      t.right = None
  else:
    t.left = prune(t.left,ne)
    t.right= prunt(t.right,ne)
  return t

def different(leftAll, rightAll, objs, ne):
  sample = objs(leftAll[0])
  rights = [seen() for _ in sample] # do i need a seen or just a list?
  lefts  = [seen() for _ in sample]
  for one in rightAll:
    [right + x for right,x in zip(rights, objs(one))]
  for one in leftAll:
    [left  + x for left ,x in zip(lefts,  objs(one))]
  for left,right in zips(left,rights): 
    if ne(left,right):
      return True
  return False
 
def tree(lst, objs,  s=None, f=0.25):
  seens  =  [seen(pos) for pos,_ in  enumerate(objs(lst[0]))]
  for one in lst:
    [see + obj for see,obj in zip(seens,objs(one))]
  return node(lst, objs, 
                 sorted(seens), 

def node(lst,objs,splits,min):
  class o:
    def __init__(i,**d): i.__dict__.update(d)
  if len(lst) < min: 
    return o(contents=lst)
  elif not splits: 
    return tree(lst,objs,min)
  else:
    head = splits.pop(0) 
    rest = splits
    left, right = [], []
    here =  o(split=median, pos=pos, all=lst[:], left=None, right=None])
       what  = left if x <= head.median() else right
       what += [one]
    here.left  = node(rest, left)
    here.right = node(rest, right)
    return here

