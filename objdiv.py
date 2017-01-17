from num import num

class N:
  def __init__(i,here):
    i.here, i.left, i.right = here, None, None

# need a post-prune

def objdiv(lst, objs,  min=None):
  for one in lst:
    nums  = objs(one)
    seens = seens  or [num(pos=i) # this is the wrong i
                       for i,_ in enumerate(nums)]
    [seen + x for seen,x in zip(seens,nums)]
  seens = sorted(seens, reverse=True, key= lambda x:x.sd())
  return objDiv1(lst,objs, seens, min or len(lst)**0.5)

def objDiv1(lst,obs,seens,min):
  if len(lst) < min: 
    return N(lst)
  elif not seens: 
    return objdiv(lst,objs,min)
  else:
    n,here,left,right = N(lst), seen[0],[],[]
    for one in lst:
       x     = one[here.pos]
       what  = left if x <= here.mu else right
    n.left  = objDiv1(seens[1:], left)
    n.right = objDiv2(seens[1:], right)
    return n

