from eg import eg
from cliffsDelta import cd,basic,optimized
from random import random as r

@eg
def cd0():
  base = [r()*10 for _ in range(30)]
  print([round(x,4) for x in sorted(base)])
  for n in range(1,8,1):
      other = [x+ (r()*n/2) for x in base]
      print(n/2, cd(base, other))
         
@eg
def _fastWorks():
  "check that the slow and fast CD  methods above give the same results"
  import random,time,sys
  one=two=0
  r = 100
  n = int(sys.argv[1]) if len(sys.argv)> 1 else 20
  m = int(sys.argv[2]) if len(sys.argv)> 2 else 1000
  for _ in range(r):
    lst1= [random.random() for _ in range(m)]
    lst2= [random.random() for _ in range(m)]
    t1  =time.process_time()
    lt1,gt1,n1= basic(lst1,lst2)
    t2  = time.process_time()
    lt2,gt2,n2= optimized(lst1,lst2) # fast=True)
    t3  = time.process_time()
    one += (t2-t1)
    two += (t3-t2)
    assert lt1==lt2, "less wrong"
    assert gt1==gt2, "more wrong"
    assert n1==n2 ,  "n wrong"
  print("repeats:",r, "listSize:",m,"slow:", one,"fast:", two,"slow/fast:",int(one/two))
  assert two < one/10

if __name__ == "__main__": eg()

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

```python
```

