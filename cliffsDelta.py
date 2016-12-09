# cliffs delta
# Tim Menzies http://menzies.us

# Returns True if two lists of numbers are different by only a trivially small
# amount.

#### Usage ##################
# from cliffsDelta import cliffsDelta

#### Notes ##################
# This file includes a simple (and slow) version of cliffsDelta plus a trickier
# (and faster) one that takes advantage of sorted lists and repeated values.

# As shown by the sampel code at bottom...

# - both give the same results
# - when using pypy3, for lists less that 512 in size, there is little difference.
# - when using python, lsts on size 2n take twice as long with cdSimple than with cdTricky

# So, it is recomended that:

# - use pypy3
# - use cdTricky

############
# Reference
# Romano, Jeanine, et al. "Exploring methods for evaluating group differences
# on the NSSE and other surveys: Are the t-test and Cohen’sd indices the most appropriate
# choices." annual meeting of the Southern Association for Institutional Research. 2006.
# small = 0.147
# medium= 0.33
# large = 0.474

def cliffsDelta(lst1,lst2, trivial=0.147, fast=True):
  f       = cdTricky if fast else cdSimple
  lt,gt,n = f(lst1,lst2)
  return abs(gt-lt) / (n + 1e-32) <= trivial

def cdSimple(lst1,lst2):
  "Simple, shows basic idea"
  lt=gt=n=0
  for x in lst1:
    for y in lst2:
      n += 1
      if x > y: gt +=1
      if x < y: lt +=1
  return lt,gt,n

def cdTricky(lst1,lst2):
  "Trickier. Not novice friendly"
  def runs(lst):
    "Reduce runs of repeats to count,item."
    for j,two in enumerate(lst):
      if j == 0:
        one,i = two,0
      if one!=two:
        yield j - i,one
        i = j
      one = two
    yield j - i + 1,two
  m, n = len(lst1), len(lst2)
  lst2 = sorted(lst2)
  j = gt = lt = 0
  for repeats,x in runs(sorted(lst1)):
    while j <= (n - 1) and lst2[j] <  x: 
      j += 1
    gt += j*repeats
    while j <= (n - 1) and lst2[j] == x: 
      j += 1
    lt += (n - j)*repeats
  return lt,gt,m*n

if __name__ == "__main__":
  # check that the two methods above give the same results
  import random,time,sys
  one=two=0
  n = int(sys.argv[1]) if len(sys.argv)> 1 else 20
  m = int(sys.argv[2]) if len(sys.argv)> 2 else 1000
  for _ in range(n):
    lst1= [random.random() for _ in range(m)]
    lst2= [random.random() for _ in range(m)]
    t1  =time.time()
    lt1,gt1,n1= cdSimple(lst1,lst2)
    t2  = time.time()
    lt2,gt2,n2= cdTricky(lst1,lst2)
    t3  = time.time()
    one += (t2-t1)
    two += (t3-t2)
    assert lt1==lt2, "less wrong"
    assert gt1==gt2, "more wrong"
    assert n1==n2 ,  "n wrong"
  print("repeats:",n, "listSize:",m,"slow:", one,"fast:", two,"slow/fast:",int(one/two))


"""
bash$ for((i=32;i<=4096;i*=2)); do pypy3 cliffsDelta.py 20 $i; done

repeats: 20 listSize:   32 slow: 0.004853010177612305  fast: 0.001377105712890625  slow/fast:  3
repeats: 20 listSize:   64 slow: 0.005321025848388672  fast: 0.005502939224243164  slow/fast:  0
repeats: 20 listSize:  128 slow: 0.00728917121887207   fast: 0.012558698654174805  slow/fast:  0
repeats: 20 listSize:  256 slow: 0.015013694763183594  fast: 0.01260066032409668   slow/fast:  1
repeats: 20 listSize:  512 slow: 0.04592585563659668   fast: 0.012231826782226562  slow/fast:  3
repeats: 20 listSize: 1024 slow: 0.17556524276733398   fast: 0.01627969741821289   slow/fast: 10
repeats: 20 listSize: 2048 slow: 0.6893131732940674    fast: 0.021253585815429688  slow/fast: 32
repeats: 20 listSize: 4096 slow: 2.738584518432617     fast: 0.035828590393066406  slow/fast: 76

bash$ for((i=32;i<=4096;i*=2)); do python3 cliffsDelta.py 20 $i; done

repeats: 20 listSize:   32 slow:  0.002935171127319336 fast: 0.0006208419799804688 slow/fast:   4
repeats: 20 listSize:   64 slow:  0.012328147888183594 fast: 0.001199483871459961  slow/fast:  10
repeats: 20 listSize:  128 slow:  0.05381202697753906  fast: 0.002763509750366211  slow/fast:  19
repeats: 20 listSize:  256 slow:  0.20172977447509766  fast: 0.005291461944580078  slow/fast:  38
repeats: 20 listSize:  512 slow:  0.8030092716217041   fast: 0.01227259635925293   slow/fast:  65
repeats: 20 listSize: 1024 slow:  3.2127115726470947   fast: 0.02505207061767578   slow/fast: 128
repeats: 20 listSize: 2048 slow: 12.957298517227173    fast: 0.05299973487854004   slow/fast: 244
repeats: 20 listSize: 4096 slow: 52.087289333343506    fast: 0.10979938507080078   slow/fast: 474

"""
