"""

Returns True if two lists of numbers are different by only a trivially small amount.

This is a non-parametric effect size test. Computes the probability that list2 has smaller
or larger numbers than list1. Two lists are the same if that probability is less
tha some `trivial` amount.

The size of `trivial` can be adjusted by an optional third argument.
The following values for this argument are recommented:

- large  = 0.474
- medium = 0.33
- small  = 0.147 
     - Use this one to test that lists are different by more than a small effect.
     - This is the default value.
 

### Reference:

Romano, Jeanine, et al. [Exploring methods for evaluating group differences on
the NSSE and other surveys: Are the t-test and Cohen's d indices the most
appropriate
choices](http://www.coedu.usf.edu/main/departments/me/documents/methodsforevaluatinggroup.pdf),
Annual meeting of the Southern Association for Institutional Research. 2006.


### Example

This example compare two lists that differ by an ever growing amont.
Note that, until we starting adding more than about 1.5, the two
lists are deemed to be the same.

      from cliffsDelta import cliffsDelta
      from random import random as r
      #
      base = [r()*10 for _ in range(30)]
      print([round(x,4) for x in sorted(base)])
      for n in range(1,8,1):
        other = [x+ (r()*n/2) for x in base]
        print(n/2, 
              cliffsDelta(base, other))

      # output
      [0.0211, 0.2545, 0.2835, 0.2904, 0.3059, 0.9386, 
       1.3436, 2.166, 2.2169, 2.2876, 2.5507, 3.812, 
       4.2212, 4.3277, 4.3789, 4.4539, 4.4949, 4.9544, 
       4.9581, 5.4141, 6.5159, 7.2154, 7.6228, 7.6377, 
       7.8872, 8.3577, 8.4743, 9.0143, 9.3915, 9.4527]
        0.5 True   
        1.0 True
        1.5 False   # <=== first time we see a difference.
        2.0 False
        2.5 False
        3.0 False
        3.5 False


______
## Programmer's guide
"""

# Returns `True` if two lists of numbers are similar.
def cd(lst1,lst2, trivial=0.147, fast=True):
  """
  This file includes a simple (and slow) version of cliffsDelta plus a trickier
  (and faster) one that takes advantage of sorted lists and repeated values.

  As shown by the [_fastWorks](cliffsDeltaeg.py) function 
  (in the test file):

  - both give the same results
  - when using pypy3, for lists less that 512 in size, there is little difference.
  - when using python, lsts on size 2n take twice as long with cdSimple than with
    cdTricky
  """
  f = optimized if fast else basic
  lt,gt,n = f(lst1,lst2)
  return (abs(gt-lt) / (n + 1e-32)) < trivial

# _______
# ### Two methods for colelcting the required stats.

# Method #1: simple, slow. Shows the basic idea.
def basic(lst1,lst2):
  lt=gt=n=0
  for x in lst1:
    for y in lst2:
      n += 1
      if x > y: gt +=1
      if x < y: lt +=1
  return lt,gt,n

# Method #2: trickier, much faster method.
# Not novice friendly.
# Exploits sorted lists, repeated values.
def optimized(lst1,lst2):  
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

#_____
# ### Helper function
# Generator.  Yields runs of repeated items as  count,item.
def runs(lst): 
    for j,two in enumerate(lst):
      if j == 0:
        one,i = two,0
      if one!=two:
        yield j - i,one
        i = j
      one = two
    yield j - i + 1,two
