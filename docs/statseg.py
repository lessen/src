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


from eg import eg
from numbers import *
from thing import thing
import time


@eg
def _different(m=512):
  rseed(17)  
  times={}
  for sd0 in range(0,10,2):
    sd = sd0/5
    one = lambda z: r()*z + (-1 if r() <0.5 else 1)*random.gauss(0,sd)
    print("")
    pops = {}
    for n0 in range(0,20,2):
      n       = n0/10
      pops[n] = thing([one(n) for _ in range(m)])
    p1 = pops[1.0]
    for n in sorted(pops.keys()):
       print(n,end=" ")
    print(" :  sd = "+str(sd/10))
    for f in [p1.cliffsDelta,p1.bootstrap,p1.same_CD,
              p1.hedges, p1.ttest,p1.same_HT]:
      name = f.__name__
      for n in sorted(pops.keys()):
        rseed(17)
        p0 = pops[n]
        time1 = time.time()
        tmp = f(p0)
        time2 = time.time()
        times[name] = times.get(name,0) + time2 - time1
        print(" * " if tmp else "   ",end=" ")
      print(" : ",name)
  times = sorted([(v,f) for f,v in times.items()])
  for v,f in times:
    print(int(v)+1,"\t",1+int(v/times[0][0]),"\t",f)
"""
Output: note that everyone agrees that if
population1 is 1*population2, then they are all the same.

But as pop2 grows more/less than x*population2, then
more and more they are the same. 

Also, as we increase standard deviation, it is more
likely that all the values are the same.

-----| _different |-----------------------

0.0 0.2 0.4 0.6 0.8 1.0 1.2 1.4 1.6 1.8  :  sd = 0.0
                     *                   :  cliffsDelta
                     *                   :  bootstrap
                     *                   :  sureSame
                 *   *   *               :  hedgesTest
                     *                   :  ttest
                     *                   :  same

0.0 0.2 0.4 0.6 0.8 1.0 1.2 1.4 1.6 1.8  :  sd = 0.1
             *   *   *   *   *           :  cliffsDelta
                 *   *   *               :  bootstrap
                 *   *   *               :  sureSame
         *   *   *   *   *   *   *   *   :  hedgesTest
                 *   *   *               :  ttest
                 *   *   *               :  same

0.0 0.2 0.4 0.6 0.8 1.0 1.2 1.4 1.6 1.8  :  sd = 0.2
 *   *   *   *   *   *   *   *   *   *   :  cliffsDelta
                 *   *   *       *       :  bootstrap
                 *   *   *       *       :  sureSame
 *   *   *   *   *   *   *   *   *   *   :  hedgesTest
                 *   *   *               :  ttest
                 *   *   *               :  same

0.0 0.2 0.4 0.6 0.8 1.0 1.2 1.4 1.6 1.8  :  sd = 0.3
 *   *   *   *   *   *   *   *   *   *   :  cliffsDelta
                 *   *   *   *   *       :  bootstrap
                 *   *   *   *   *       :  sureSame
 *   *   *   *   *   *   *   *   *   *   :  hedgesTest
                 *   *   *   *           :  ttest
                 *   *   *   *           :  same

0.0 0.2 0.4 0.6 0.8 1.0 1.2 1.4 1.6 1.8  :  sd = 0.4
 *   *   *   *   *   *   *   *   *   *   :  cliffsDelta
     *   *   *   *   *   *       *   *   :  bootstrap
     *   *   *   *   *   *       *   *   :  sureSame
 *   *   *   *   *   *   *   *   *   *   :  hedgesTest
         *   *   *   *   *               :  ttest
         *   *   *   *   *               :  same
"""

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

