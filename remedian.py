# remedian: incrementally find median.
# Copyright (c) 2016, Tim Menzies, BSD (2-Clause).

# Implemented via a set of lists. New numbers are added
# to lst[i] and when it fills up, it posts its median
# to lst[i+1]. When a remedian is queried for the current
# median, it returns the median of the last list with any
# numbers.

# Example usage:

#    z=remedian()
#    for i in range(1000):
#      z + i
#      if not i % 100:
#        print(i, z.median())

# Based on The Remedian:A Robust Averaging Method for Large Data Sets
# Peter J. Rousseeuw and Gilbert W. Bassett Jr.
# Journal of the American Statistical Association
# March 1990, Vol. 85, No. 409, Theory and Methods
# http://web.ipac.caltech.edu/staff/fmasci/home/astro_refs/Remedian.pdf

# The test code (at bottom) compares this rig to
# 1) using Python's built-in sort
# 2) then reporing the middle number
#
# When using pypy, and assuming lists of length 64, remedian is about 30% faster than
# raw sort after 500 items (while at the same time, avoids
# having to store all the numbers in RAM).
#
# Further, remedian's computed median is within 1% (or less)
# of the medians found via Python's sort.

class remedian:
  def __init__(i,k=64,  # after some experimentation, 64 works ok
               lvl=0):
    i.all,i.k,i.lvl = [],k,lvl
    i.more,i._median=None,None
  def __add__(i,x):
    i._median = None
    i.all.append(x)
    if len(i.all) == i.k:
      i.more = i.more or remedian(lvl = i.lvl+1,k=i.k)
      i.more + i.median0(i.all)
      i.all = []
  def median(i):
    return i.more.median() if i.more else i.median0(i.all)
  def median0(i,lst):
    if not i._median:
      n  = len(lst)
      p  = q  = n//2
      if n < 3:
        p,q = 0, n-1
      else:
        lst.sort()
        if not n % 2:
          q = p -1
      i._median = lst[p] if p==q else (lst[p]+lst[q])/2
    return i._median
        
if __name__ == '__main__':
  import random,time
  random.seed(1)
  r=random.random
  q=lambda z:round(z,4)
  # ---------------------------------
  # test0: basic usage
  
  z=remedian()
  for i in range(1000):
     z + i
     if not i % 100:
        print(i, z.median())
        
  # ---------------------------------
  # test1: just something simple
  
  z=remedian()
  lst=[r()**2 for _ in range(1000)]
  [z + x for x in lst]
  print(z.median(), sorted(lst)[500])
  
  # ---------------------------------
  # test2: store increasing amount of numbers
  #        with different values for k
  
  for k in [8,16,32,64,128]:
    print("")
    for f in range(0,4):
      n = 50*10**f
      repeats,terr,merr,tall = 100,0,0,0
      for _ in range(repeats):
        z=remedian(k=k)
        lst = [r()**2 for _ in range(n)]
        t1=time.time()
        for x in lst:
          z + x
        m1 = z.median()
        t2 = time.time()
        m2 = sorted(lst[:])[n//2]
        t3 = time.time()
        merr += m1/m2
        terr += (t2-t1)/(t3-t2)
        tall += (t2-t1)
      print(dict(k=k,n=n,
                 runtTime=       q(tall/repeats),
                 medianError=    q(merr/repeats),
                 timeDifference= q(terr/repeats)))

"""
> time pypy3 remedian.py
0 0
100 31.5
200 95.5
300 127.5
400 191.5
500 223.5
600 287.5
700 319.5
800 383.5
900 447.5
0.2676937558483627 0.2715219408536629

{'k': 8, 'n': 50, 'runtTime': 0.0002, 'medianError': 1.0223, 'timeDifference': 17.1506}
{'k': 8, 'n': 500, 'runtTime': 0.0004, 'medianError': 1.0341, 'timeDifference': 5.38}
{'k': 8, 'n': 5000, 'runtTime': 0.0007, 'medianError': 1.0299, 'timeDifference': 0.9414}
{'k': 8, 'n': 50000, 'runtTime': 0.004, 'medianError': 1.0305, 'timeDifference': 0.4372}

{'k': 16, 'n': 50, 'runtTime': 0.0002, 'medianError': 0.949, 'timeDifference': 51.1795}
{'k': 16, 'n': 500, 'runtTime': 0.0002, 'medianError': 1.0058, 'timeDifference': 2.5798}
{'k': 16, 'n': 5000, 'runtTime': 0.0006, 'medianError': 1.0126, 'timeDifference': 0.8711}
{'k': 16, 'n': 50000, 'runtTime': 0.0042, 'medianError': 1.0072, 'timeDifference': 0.4731}

{'k': 32, 'n': 50, 'runtTime': 0.0, 'medianError': 0.9977, 'timeDifference': 2.2678}
{'k': 32, 'n': 500, 'runtTime': 0.0001, 'medianError': 0.9941, 'timeDifference': 1.0468}
{'k': 32, 'n': 5000, 'runtTime': 0.0005, 'medianError': 0.9958, 'timeDifference': 0.7138}
{'k': 32, 'n': 50000, 'runtTime': 0.0043, 'medianError': 1.0009, 'timeDifference': 0.5116}

{'k': 64, 'n': 50, 'runtTime': 0.0, 'medianError': 0.9652, 'timeDifference': 2.685}
{'k': 64, 'n': 500, 'runtTime': 0.0, 'medianError': 0.9904, 'timeDifference': 0.8901}
{'k': 64, 'n': 5000, 'runtTime': 0.0005, 'medianError': 0.9982, 'timeDifference': 0.7761}
{'k': 64, 'n': 50000, 'runtTime': 0.0046, 'medianError': 1.0019, 'timeDifference': 0.5482}

{'k': 128, 'n': 50, 'runtTime': 0.0, 'medianError': 0.9634, 'timeDifference': 2.5693}
{'k': 128, 'n': 500, 'runtTime': 0.0, 'medianError': 0.9898, 'timeDifference': 0.9376}
{'k': 128, 'n': 5000, 'runtTime': 0.0005, 'medianError': 0.9989, 'timeDifference': 0.7821}
{'k': 128, 'n': 50000, 'runtTime': 0.0054, 'medianError': 0.9998, 'timeDifference': 0.6213}

real	0m8.749s
user	0m8.407s
sys	0m0.280s
"""
