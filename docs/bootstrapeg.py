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


from random    import random as r
from bootstrap import bootstrap as bst
from time      import process_time as now
import random

def base0(n):
  return [r() for _ in range(n)]

@eg
def _b0(n=30,div=100, boo=bst,same=None,f=base0):
  print(boo.__name__)
  base = f(n)
  same0 = None
  t0 = None
  other=None
  for conf in [90,95,99]:
    print("")
    for b in [32,64,128,256,512,1024]:
      report=[]
      t=0
      for n in range(0,10,2):
        other   = [x+ (r()*n/div) for x in base]
        t1      = now()
        same    = boo(base, other,b=b,conf=conf)
        same0   = same if same0 == None else same0
        t2      = now()
        t      += t2 - t1
        report += ["=" if same else "."]
      t0 = t if t0 == None else t0
      print(''.join(report),dict(conf=conf,b=b,time=round(t/t0,2)))
  print("list first:",[round(x,2) for x in sorted(base)[::2]])
  print("list  last:",[round(x,2) for x in sorted(other)[::2]])
  assert same0,"first must be the same"
  assert not same,"last should be different"
        
@eg
def _b1():
  for k in [0.5,1,2,4]:
    print("")
    print(dict(shape=k))
    f = lambda n: [random.weibullvariate(1,k)
                   for _ in range(n)]
    _b0(f=f)
  
  
if __name__ == "__main__": eg()

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

