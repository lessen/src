
# bootstrap


Returns true if two lists are not statistically significantly different.

Based on [An introduction to the
bootstrap](https://github.com/timm/timm.github.io/blob/master/pdf/93bootstrap.pdf)
by Bradley Efron, 1993, Chapman and Hall, page 220 to 223.

Works via `bootstrap sampling` which Effron describes as a variant of the Fisher
permutation test:

- A magic number, the achieved significance level (ASL) is caluclated 
  from numerous random samples of the original lists (and,
  by sample, Effron means "sample with replacement").
- The _larger_ the ASL, the weaker the evidence _against_ the null
  hypothesis (that the two lists belong to the same distribution);
- I.e. the larger the ASL, we more we can believe in the lists are the same.

The importance of this method is that, unlike standard statistical hypothesis
tests, there is no assumption here that the distributions come from some known
distribution (e.g. the normal distribution).

____

## Programmer's Guide


```python
import random
  
def bootstrap(y0,z0, b = 256, conf= 95):
  tiny=1e-32 # added to some divisions to stop div zero errors

  # ### Helpers

  # Return any number 0 to n
  def any(n): return random.uniform(0,n)

  # Return any list item (uses `any`).
  def one(lst): return lst[ int(any(len(lst))) ]
  
  # Return any sample from `lst` (uses `one`).
  def sampleWithReplacement(lst):
    return [one(lst) for _ in lst]
  
  # The test statistic: comments on the difference between two lists
  def testStatistic(y,z): 
    tmp1 = tmp2 = 0
    for y1 in y.all: tmp1 += (y1 - y.mu)**2 
    for z1 in z.all: tmp2 += (z1 - z.mu)**2
    s1    = (tmp1 / (y.n - 1 + tiny))**0.5
    s2    = (tmp2 / (z.n - 1 + tiny))**0.5
    delta = abs(z.mu - y.mu)
    if s1+s2:
      delta =  delta/((s1/(y.n + tiny) + s2/(z.n + tiny))**0.5)
    return delta
  
  #______
  # ### Num class
  
  # A counter class to simplify reasoning about sets of numbers
  class num():
    def __init__(i,some=[]):
      i.sum = i.n = i.mu = 0 ; i.all=[]
      for one in some:
        i.put(one)
    def put(i,x):
      i.all.append(x);
      i.sum +=x; i.n += 1
      i.mu   = i.sum/(i.n + tiny)
    def __add__(i1,i2):
      return num(i1.all + i2.all)
 
  # -------------------------
  # ### Run this script
  
  # Some set up
  y, z   = num(y0), num(z0)
  x      = y + z
  tobs   = testStatistic(y,z)

  # Effron recommends adjusting all the populations so they have the same mean
  yhat   = [y1 - y.mu + x.mu for y1 in y.all]
  zhat   = [z1 - z.mu + x.mu for z1 in z.all]
  
  # Compute the achieved significance level.
  asl = tiny
  for _ in range(b):
    if testStatistic(num(sampleWithReplacement(yhat)),
                     num(sampleWithReplacement(zhat))) > tobs:
      asl += 1/b

  # The larger the `asl` value, the more likely it
  # is `True` that the lsts are the same.
  # print("bb",asl,conf/100)
  return asl > conf/100

```


___ 

## FAQ

Why is the last line above  `asl > conf/100` and not `asl < conf/100`?

This is because of the way Efrom defines `asl` 
(the _larger_ the ASL, the weaker the evidence that the lists
are different). Chapter 16 of his text explains that in more detail.

(Aside: since I am not a very trusting soul, I have coded this up reversing
 &gt; with &lt;. When I did, `bootstrap` produced the reverse
of the expected results.)


```python
```

