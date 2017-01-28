from median import median
from eg import eg
import time
from random import random as r

@eg
def _med():
  "pre-sorting lists only really useful for large lists (over 10,000) items"
  assert median([1,2,3,4,5]) == 3
  assert median([1,2,4,5]) == 3
  for pow in range(2,7):
    slow=fast=0
    for i in range(100):
      size=int(r()*10**pow)
      if size < 1: continue
      lst1 = [x for x in range(size)]
      lst2 = sorted(lst1[:])
      t1 = time.process_time()
      n1 = median(lst1,ordered=False)
      t2 = time.process_time()
      n2 = median(lst2,ordered=True)
      t3 = time.process_time()
      assert n1==n2
      fast += t3-t2
      slow += t2-t1
    print("size: %10s slow: %8.5f fast: %8.5f slow/fast: %8.5f " % (
          10**pow,slow, fast, slow/fast))

if __name__ == "__main__": eg()
