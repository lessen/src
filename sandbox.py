def streamingMedian(seq,epsilon=0.001):
   m = 0
   seq =iter(seq)
   hi,lo = 0,1e32
   for nextElt in seq:
      hi = max(nextElt,hi)
      lo = min(nextElt,lo)
      delta= abs(hi-lo)*epsilon
      #delta = 1
      if m > nextElt:
         m -= delta
      elif m < nextElt:
         m += delta
      yield m

def naturalNumbers():
   n = 1
   while True:
      yield n
      n += 1

def novel(seq,epsilon=0.05):
  v1 = next(seq)
  n=0
  while True:
    n +=1 
    v2 = next(seq)
    if (v2 - v1)/(v1+1e-32) > epsilon:
      yield n,v2
      v1 = v2

import random

def r(n=1):
  while True:
    yield 1000*random.random()**n


for medianSoFar in novel(streamingMedian(r(0.5))):
   print(medianSoFar)
