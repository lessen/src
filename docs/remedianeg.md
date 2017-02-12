
# remedianeg

from remedian import remedian
from eg       import eg
from random import random as r
import time


@eg
def _remedian1():
  "basic usage"
  z=remedian()
  for i in range(1000):
     z + i
     if not i % 100:
        print(i, z.median())


@eg
def _remedian2():
  "test2: store increasing amount of numbers with different values for k"
  for k in [8,16,32,64,128]:
    print("")
    for f in range(0,4):
      n = 50*10**f
      repeats,terr,merr,tall = 100,0,0,0
      for _ in range(repeats):
        lst = [r()**2 for _ in range(n)]
        t1=time.process_time()
        z   = remedian(k=k)
        [z + x for x in lst]
        m1 = z.median()
        t2 = time.process_time()
        m2 = sorted(lst[:])[n//2]
        t3 = time.process_time()
        merr += m1/m2
        terr += (t2-t1)/(t3-t2)
        tall += (t2-t1)
      q=lambda z:round(z,4)
      print(dict(k=k,n=n,
               runtTime=       q(tall/repeats),
               medianError=    q(merr/repeats),
               timeDifference= q(terr/repeats)))

if __name__ == "__main__" : eg()

----| _remedian1 |----------------------------------------
# basic usage

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
# pass (0.0024 secs)

-----| _remedian2 |----------------------------------------
# test2: store increasing amount of numbers with different values for k


{'k': 8, 'n': 50, 'runtTime': 0.0002, 'medianError': 1.0115, 'timeDifference': 16.4694}
{'k': 8, 'n': 500, 'runtTime': 0.0003, 'medianError': 1.0368, 'timeDifference': 5.846}
{'k': 8, 'n': 5000, 'runtTime': 0.0017, 'medianError': 1.0378, 'timeDifference': 2.851}
{'k': 8, 'n': 50000, 'runtTime': 0.0118, 'medianError': 1.0349, 'timeDifference': 1.6066}

{'k': 16, 'n': 50, 'runtTime': 0.0, 'medianError': 0.9563, 'timeDifference': 5.3626}
{'k': 16, 'n': 500, 'runtTime': 0.0002, 'medianError': 1.0102, 'timeDifference': 3.1368}
{'k': 16, 'n': 5000, 'runtTime': 0.0008, 'medianError': 1.0088, 'timeDifference': 1.3289}
{'k': 16, 'n': 50000, 'runtTime': 0.007, 'medianError': 1.0074, 'timeDifference': 0.9513}

{'k': 32, 'n': 50, 'runtTime': 0.0, 'medianError': 0.9926, 'timeDifference': 2.3615}
{'k': 32, 'n': 500, 'runtTime': 0.0001, 'medianError': 0.9949, 'timeDifference': 1.8829}
{'k': 32, 'n': 5000, 'runtTime': 0.0006, 'medianError': 1.0061, 'timeDifference': 1.0009}
{'k': 32, 'n': 50000, 'runtTime': 0.0054, 'medianError': 1.0029, 'timeDifference': 0.7321}

{'k': 64, 'n': 50, 'runtTime': 0.0, 'medianError': 0.9644, 'timeDifference': 2.5064}
{'k': 64, 'n': 500, 'runtTime': 0.0001, 'medianError': 0.9897, 'timeDifference': 1.0117}
{'k': 64, 'n': 5000, 'runtTime': 0.0006, 'medianError': 0.9965, 'timeDifference': 0.9034}
{'k': 64, 'n': 50000, 'runtTime': 0.0047, 'medianError': 1.0004, 'timeDifference': 0.647}

{'k': 128, 'n': 50, 'runtTime': 0.0, 'medianError': 0.9634, 'timeDifference': 2.5424}
{'k': 128, 'n': 500, 'runtTime': 0.0, 'medianError': 0.9897, 'timeDifference': 0.776}
{'k': 128, 'n': 5000, 'runtTime': 0.0005, 'medianError': 0.9969, 'timeDifference': 0.8013}
{'k': 128, 'n': 50000, 'runtTime': 0.0046, 'medianError': 0.9999, 'timeDifference': 0.6258}

```python
```

