# cliffsDelta.py
# ==============
#
# Returns True if two lists of numbers are different by only a trivially small amount.
# Copyright (C) 2016, Tim Menzies BSD (2clause)
#
# Usage
# -----
#
#       from cliffsDelta import cd
#
# Notes
# -----
#
# This file includes a simple (and slow) version of cliffsDelta plus a trickier
# (and faster) one that takes advantage of sorted lists and repeated values.
#
# As shown by the sampel code at bottom...
#
# - both give the same results
# - when using pypy3, for lists less that 512 in size, there is little difference.
# - when using python, lsts on size 2n take twice as long with cdSimple than with cdTricky
#
# So, it is recomended that:
#
# - use pypy3;
# - use optimize (which is default, in the code).
#
# Reference
# ---------
#
# The following paper recommends that `trivial` be defined as follows:
#
# - small  = 0.147 (use this one to test that lists are different by more than a small effect)
# - medium = 0.33
# - large  = 0.474
#
# Romano, Jeanine, et al. _Exploring methods for evaluating group differences
# on the NSSE and other surveys: Are the t-test and Cohen’sd indices the most appropriate
# choices._ annual meeting of the Southern Association for Institutional Research. 2006.
#
# ____________________________________________________________________________________

def cd(lst1,lst2, trivial=0.147, fast=True):
  "Returns True if two lists of numbers are similar."
  f = optimized if fast else basic
  lt,gt,n = f(lst1,lst2)
  return (abs(gt-lt) / (n + 1e-32)) < trivial

def basic(lst1,lst2):
  "Simple, shows basic idea"
  lt=gt=n=0
  for x in lst1:
    for y in lst2:
      n += 1
      if x > y: gt +=1
      if x < y: lt +=1
  return lt,gt,n

def optimized(lst1,lst2):
  "Trickier. Not novice friendly. Exploits sorted lists, repeated values."
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

