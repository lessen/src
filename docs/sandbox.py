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




def det(**d):
   k,v = next(iter(d.items()))
   return globals()[k] if k in globals() else v

print(det(a=1))
b=2
print(det(b=10))

def streamingMedian(seq,epsilon=0.001,pause=100):
   n = sd= 0
   mu =m2=0
   seq =iter(seq)
   lo,hi=1e32,-1e32
   for x in seq:
     n  += 1
     delta = x - mu
     mu += delta/n
     m2 += delta*(x - mu)
     lo=min(lo,x)
     hi=max(hi,x)
     delta=(hi - lo)*epsilon
     if n < pause:
       m    = mu
     else:
       sd = (m2/(n-1))**0.5
       if m > x:
         m -= sd*0.1
       elif m < x:
         m += sd*0.1
     yield m,n,sd

def naturalNumbers():
   n = 1
   while True:
      yield n
      n += 1

def novel(seq,epsilon=1.1):
  _,v1,_ = next(seq)
  while True:
    n,v2,sd = next(seq)
    if (v2 - v1)/(v1+1e-32) > epsilon:
      yield v2,n,sd
      v1 = v2

import random

def r(n=1,m=100000):
  j = 0
  while j < m :
    j += 1
    yield random.random()**n


random.seed(1)
for n,v,sd in novel(streamingMedian(r(2))):
   print("%10s %10.5f %s" % (n, v, ("*" * int(v*100))),0.2*sd)
  

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

