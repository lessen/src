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


Maintains summaries of symbols. Can be used incrementally, or in batch.

Example of incremental usage:

        words = # some long list of quotes
        words = re.sub(r'[-,\.\n]'," ",words).split()

        s=sym()
        for i,x in enumerate(words):
            s + x
            if i % 25 == 0: print(s) 
        print(s)

        # output:
        {:n   1 :most  1 :mode You :ent 0}
        {:n  26 :most  3 :mode is  :ent 4.1329}
        {:n  51 :most  4 :mode is  :ent 5.0546}
        {:n  76 :most  5 :mode is  :ent 5.495}
        {:n 101 :most  7 :mode the :ent 5.8595}
        {:n 126 :most  7 :mode the :ent 6.2548}
        {:n 151 :most 10 :mode is  :ent 6.2816}
        {:n 176 :most 12 :mode is  :ent 6.3449}
        {:n 199 :most 13 :mode is  :ent 6.5374}

Example of batch usage:

       print( sym( x for x in words ))

       # output:
       {:n 199 :most 13 :mode is :ent 6.5374}

Also, can be used to:

- compute distance between symbols (used in nearest-neighbor calculations);
- compute likelihood a symbol belongs to a sample (used in Bayes classifiers).

____

## Programmer's Guide
"""

from math import log

class sym:

  # Initialization
  def __init__(i,inits=[]):
    i.n, i.most, i.mode, i.counts = 0,0,None,{}
    [i + x for x in inits]

  # Reporting
  def __repr__(i):
    return '{:n %s :most %s :mode %s :ent %.5g}' % (i.n,i.most,i.mode,i.ent())

  # Updating. If we find a new most frequent symbol, update `mode`.
  def __add__(i,x):
    i.n += 1
    count= i.counts[x] = i.counts.get(x,0) + 1
    if count > i.most:
      i.most,i.mode=count,x
    return x

  # Entropy calculation (guesstimate of the number of bits required to encode this distribution).
  def ent(i):
    e = 0
    for _,v in i.counts.items():
      p  = v/i.n
      e -= p*log(p,2)
    return e

  #----------------------------------------------------------------------------
  # ### Distance calculations
  
  # Distance between two symbols, defined as per p42 of [Aha et al., 1991](https://goo.gl/2722eJ)
  # (when faced with unknown values, assume maximal distance).
  def dist(i,x,y,miss="?"):
    if   x == miss and y == miss : return None
    elif x == miss or  y == miss : return 1
    else:
      return 0 if x==y else 1
  
  # Calculates how likely is it that symbol `x` belongs to this distribution (used in Bayes classifiers).
  # Adds certain magic factors to the numerator and denominator to handle low frequency events.
  # From Section 3 of [Yang and Webb,2002](http://i.giwebb.com/wp-content/papercite-data/pdf/YangWebb02b.pdf).
  def like(i,x,prior=0,m=2):
     return (i.counts.get(x,0) + m*prior)/(i.n + m)   
 

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

