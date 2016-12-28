from table  import table
from random import shuffle,random
from abcd   import abcd
from numerr import numerr

def  xval(t,m=5,n=5,prefix="",classification=True,*lst,**d):
    logger = abcd if classification else numerr
    all    = t.rows[:]
    width  = int(len(t.rows)/i.n)
    for m1 in range(m):
      random.shuffle(all)
      for n1 in range(n):
        lo = width * n1
        hi = width * (n1 + 1)
        training = t.twin(all[0:lo] + all[hi:])
        testing  = t.twin(all[lo:hi])
        logger   = logger(prefix)
        yield m1,n1,training,testing,logger
        
