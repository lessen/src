from num import num

# need a post-prune

def objdiv(lst, objs,  min=None):
  for one in lst:
    meds = meds  or [(remedian(),i) for i,_ in enumerate(objs(one))]
    [med + objs(one)[i] for med,i in meds]
  meds = sorted(meds, reverse=True, key= lambda x:x[0].median())
  return objDiv1(lst,objs, seens, min or len(lst)**0.5)

def objDiv1(lst,obs,seens,min):
  class o:
    def __init__(i,**d): i.__dict__.update(d)
  if len(lst) < min: 
    return o(contents=lst)
  elif not seens: 
    return objdiv(lst,objs,min)
  else:
    n, ,(med,i), left, right = o(contents=lst), seen[0], [], []
    for one in lst:
       x     = objs(one)[i]
       what  = left if x <= med.median() else right
    n.left  = objDiv1(seens[1:], left)
    n.right = objDiv2(seens[1:], right)
    return n

