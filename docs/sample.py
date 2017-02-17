""" 
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-55634425-2', 'auto');
  ga('send', 'pageview');

</script>
<img 
src="https://avatars0.githubusercontent.com/u/23156192?v=3&s=200"
align=left
width=120>
&nbsp;<br>&nbsp;<br>
&nbsp;&nbsp; [home](http://ttv1.github.io) | [discuss](#discussion) | [report bug](https://github.com/ttv1/src/issues) 


<br clear=all>

_________________


Maintains a random sample
of items.  Can be used incrementally, or in batch.

Example of incremental usage:

        s=sample()
        for i in range(1000):
          s + i
          if i % 100 == 0: print(s,s.stats())

        # output:
        {:n 1 :len 1 :some [0]} (0, 0)
        {:n 101 :len 101 :some [0, 1, 2, 3, 4]} (50, 50)
        {:n 201 :len 201 :some [0, 1, 2, 3, 4]} (100, 100)
        {:n 301 :len 256 :some [0, 1, 2, 4, 5]} (149.5, 154)
        {:n 401 :len 256 :some [0, 1, 2, 4, 7]} (197.5, 205)
        {:n 501 :len 256 :some [0, 1, 7, 8, 9]} (251.5, 249)
        {:n 601 :len 256 :some [0, 8, 9, 10, 16]} (311.0, 287)
        {:n 701 :len 256 :some [8, 9, 10, 16, 18]} (353.5, 362)
        {:n 801 :len 256 :some [8, 9, 10, 16, 18]} (413.5, 415)
        {:n 901 :len 256 :some [8, 9, 10, 16, 18]} (462.5, 450)

Example of batch usage     

        s= sample(i for i in range(901))
        print(s,s.stats())

        # output
        {:n 901 :len 256 :some [2, 12, 14, 15, 16]} (480.5, 443

Also, can be used to:

- build a (small) cache of values that can be used in some subsequent analysis
- compute parametric tests for effect size and statistical hypothesis checking

_____
## Programmer's Guide    
"""

from random import random as r
from cliffsDelta import cd
from bootstrap   import bootstrap

class sample:
  SAMPLES = 256

  # Initialization
  def __init__(i,inits=[],samples=None):
    i.max = samples or sample.SAMPLES
    i.some,i.n= [],0
    i._median= None
    [i + x for x in inits]
    
  # Reporting
  def __repr__(i):
    return "{:n %s :len %s :some %s}" % (i.n, len(i.some), i.some[:5])
  
  # Updating. Keeps new items a probability
  # determined by the number of items seen.
  # If `some` is full, replace a random item.
  # `_median` is wiped since it now out of date.
  def __add__(i,x):
    i._median= None
    i.n += 1
    now = len(i.some)
    if now < i.max:
      i.some += [x]
    elif r() <= now/i.n:
      i.some[ int(r() * now) ]= x

  # ---------------------------------------------------------
  # ### Statistics

  # Return stats
  def stats(i):
    return i.median(), i.iqr()
  
  # Return the median of the sample. Cache that value since
  # it is somewhat expensive to compute. Assumes list is all
  # numeric values
  def median(i):
    if i._median is None:
      n = len(i.some)
      p = q  = n//2 # usually we talk to the center
      if n < 3:    
        p,q = 0, n-1 # sometimes, for short lists, just use first,last
      else:
        i.some.sort()
        if not n % 2: # for even lists, return mean of middle items
          q = p -1
      i._median = i.some[p] if p==q else (i.some[p]+i.some[q])/2
    return i._median
  
  # Return the intra-quartile range (75th-25th percentile).
  def iqr(i):
    i.median() # ensure all is sorted.
    p = len(i.some) //4
    return i.some[3*p] - i.some[p]

  # Two distributions are different if they are not statistically
  # significantly similar and if they are not different by
  # just a small effect size.
  def diff(i,j):
    return not i.cliffsDelta(j) and not i.bootstrap(j)
  
  # Non-parametric statistical signifance test
  def bootstrap(i,j,b=256,conf=95):
    return bootstrap(i.some,j.some,b=b,conf=conf)
  
  # Non-parametric effect size test
  def cliffsDelta(i,j,trivial=0.147):
    return cd(i.some,j.some, trivial=trivial)


"""
____


<img align=right 
src="https://raw.githubusercontent.com/timm/timm.github.io/master/timm.png"
width=170>
## Copyleft

Copyright &copy; 2016 Tim Menzies <tim@menzies.us>

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The F*ck You Want
To Public License, Version 2, as published by Sam Hocevar. See
[http://www.wtfpl.net](http://www.wtfpl.net) for more details.

Share and enjoy.

"""

