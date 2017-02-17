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



- In use, values are just thrown at a `thing` and, internally, this code works
  out if we are talking about `num`s or `sym`s.
     - Internally, `thing`s have a variable `thing.my`s containing either a `num` or a `sym`.


- Apart from sumamries, `thing`s also keep a random `sample` of the values seen
  so far.
     - This variable is kept in `thing.samples`.

### Usage

Can be used incrementally, or in batch.

#### Example of incremental usage:

       t=thing()
       for i in range(1000):#
         t + i
         if i % 100 == 0: print(t,t.samples.stats())

        # output:
        {:txt 0 :pos 0 :n 1} (0, 0)
        {:txt 0 :pos 0 :n 101} (50, 50)
        {:txt 0 :pos 0 :n 201} (100, 100)
        {:txt 0 :pos 0 :n 301} (149.5, 154)
        {:txt 0 :pos 0 :n 401} (197.5, 205)
        {:txt 0 :pos 0 :n 501} (251.5, 249)
        {:txt 0 :pos 0 :n 601} (311.0, 287)
        {:txt 0 :pos 0 :n 701} (353.5, 362)
        {:txt 0 :pos 0 :n 801} (413.5, 415)
        {:txt 0 :pos 0 :n 901} (462.5, 450)
        {:txt 0 :pos 0 :n 901} (480.5, 443)

#### Example of batch usage:

        t= thing(i for i in range(901))
        print(t,t.samples.stats())

        # output
        {:txt 0 :pos 0 :n 69}

______
## Programmer's Guide

"""
from num     import num
from sym     import sym
from sample  import sample

class thing:
  UNKNOWN = "?"

  # Initialization
  def __init__(i,inits=[],pos=None, txt=None,samples=None):
    pos = pos or 0
    txt = txt or pos
    i.txt=str(txt)
    i.pos=pos
    i.my=None # will contain a `num` or a `sym`, depending on what data arrives
    i.samples=None
    [i + x for x in inits]

  # Pretty print
  def __repr__(i):
    return '%s{:txt %s :pos %s :n %s}' % (
              (i.my.__class__.__name__ if i.my else ""),
              i.txt,i.pos,i.n())

  # Updating. If this our first item, then work out the type
  # and initialize the internal summary variable.
  # Also, ensure we have a pace to store the random `samples`.
  def __add__(i,xs):
    for x in i.items(xs):
      if i.my is None: 
        what = num if isinstance(x,(float,int)) else sym
        i.my  = what()
      if i.samples is None:
        i.samples = sample()   
      i.my + x
      i.samples + x
    return xs

  # Iterating over items. If passed a list then yield each item.
  # Otherwise, just yield the passed in argument.
  # But do not yield anything that is an `UNKNOWN` value.
  def items(i,xs):
    xs = xs if isinstance(xs,(list,tuple)) else [xs]
    for x in xs:
      if x != thing.UNKNOWN:
        yield x
        
  # _____
  # ### Deferred services
  
  # Much of `thing`'s services are defined in terms of the nested
  # internal summary variables.
  # For example, here's how we compute 
  # the number of items seen by this `thing`. 
  def n(i):
    return i.my.n
  
  def dist(i,j,k)     : return i.my.dist(j,k)
  
  def cliffsDelta(i,j): return i.samples.cliffsDelta(j.samples)
  def ranges(i)       : return i.samples.ranges()
  def bootstrap(i,j)  : return i.samples.bootstrap(j.samples)
  def same_CD(i,j)    : return i.cliffsDelta(j)  and i.bootstrap(j) 
  

  # Parametric. assumes gaussians
  def same_HT(i,j)    : return i.hedges(j) and i.ttest(j)
  def ttest(i,j)      : return i.my.ttest(j.my)
  def hedges(i,j)     : return i.my.hedges(j.my)

  



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

