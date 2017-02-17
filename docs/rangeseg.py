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


from random import random as r
from random import seed
from eg import eg


@eg
def _div0a():
  for rng in div([ 10,11,13,14,15,15,16,16,17,
                   20,21,23,24,25,25,26,26,27,
                   30,31,33,34,35,35,36,36,37 ]):
    print("range", rng["id"],":",
                   dict(lo= rng["x"].lo,
                        hi= rng["x"].hi))

@eg
def _div0b():
  a,b  = "a","b"
  for rng in ediv([ (10,a),(11,a),(13,a),(14,a),(15,a),
                   (20,b),(21,b),(23,b),(24,b),(25,b),
                   (30,b),(31,b),(33,b),(34,b),(35,b) ]):
    print("range",rng["id"],":",
                  dict(lo= rng["x"].lo,
                       hi= rng["x"].hi))
    
@eg
def _div0c():
  for rng in sdiv([ (0.7,2),(0.75,2),(0.8,2),(0,85,2),(0.9,2),(0.8,2),(1,2),
                    (1.05,2),(1,2),(0.7,2),(0.75,2),(0.8,2),(0.85,2),(0.9,2),
                    (10,14),(10.5,13.5),(11,13),(11.5,13),(12,12.5),(12.5,12),
                    (13,11.5),(13.5,10.5),(14,10),(14.5,9.5),(15,9),(15.5,8.5)
                  ]):
    print("range",rng["id"],":",
                  dict(lo= rng["x"].lo,
                       hi= rng["x"].hi))
    
@eg
def _div0d():
  for rng in ddiv(dict(x1=[0.34, 0.49, 0.51, 0.6],
                       x2=[0.6,  0.7,  0.8,  0.9],
                       x3=[0.15, 0.25, 0.4,  0.35],
                       x4=[0.6,  0.7,  0.8,  0.9],
                       x5=[0.1,  0.2,  0.3,  0.4])):    
    print("range",rng["id"],":",
          [x[0].label for x in rng["has"]],
          dict(lo= rng["x"].lo,
               hi= rng["x"].hi))
     
@eg
def _div1(n=10000):
  "1D cluster. Noise. Should divide evenly."
  for zz in div([r() for _ in range(n)]):
    xx = zz["x"]
    print("start  %.4f stop %.4f n %s" % (xx.lo, xx.hi, xx.n))

@eg
def _div2(n=100000):
  "1D cluster. random**3: most nums below half are very similar"
  for zz in div([r()**3 for _ in range(n)]):
    xx = zz["x"]
    print("start  %.4f stop %.4f n %s" % (xx.lo, xx.hi, xx.n))

@eg
def _div3():
  "1D cluster. Small population."
  _div1(20)

def first(x): return x[0]
def second(x): return x[1]

@eg
def _sdiv(n=10000):
  "2D. Y does not change except at 33 and 66"
  def cut(x):
    more = lambda x:x + (0.1*r())
    if x < 0.33: return more(0.33)
    if x < 0.66: return more(0.66)
    return more(1)
  lst0 = [r() for _ in range(n)]
  lst = [[x, cut(x)] for x in lst0]
  for zz in sdiv(lst):
    xx = zz["x"]
    yy = zz["y"]
    print("start  %.4f stop %.4f n %s " % (xx.lo, xx.hi, xx.n),end="")
    print("xmedian %.4f ymedian %.4f" % (xx.median(), yy.median()))

@eg    
def _ediv(n=1000):
  "2D class only changes symbols at .33 and .5"
  def cut(x):
    if x < 0.33: return "a"
    if x < 0.5 : return "b"
    return "c"
  lst0 = [r()**2 for i in range(n)]
  lst = [[x, cut(x)] for x in lst0]  
  for zz in ediv(lst):
     xx = zz["x"]
     print("start  %.4f stop %.4f n %s" % (xx.lo, xx.hi, xx.n))

@eg
def _ddiv1(n=1000):
  "1D: cluster similiar things"
  data = dict(rx1 = [10*r()**3 for _ in range(n)],
              rx2 = [10*r()**0.33   for _ in range(n)],
              rx4 = [10*r()**3 for _ in range(n)],
              rx3 = [10*r()      for _ in range(n)])
  ddv0(data)

@eg
def _ddiv2(n=100):
  ddv0(dict(x1=[0.34, 0.49, 0.51, 0.6],
            x2=[6,  7,  8,  9]))
  
@eg
def _ddiv20():
  ddv0(dict(x1=[0.34, 0.49, 0.51, 0.6],
            x2=[0.6,  0.7,  0.8,  0.9],
            x3=[0.15, 0.25, 0.4,  0.35],
            x4=[0.6,  0.7,  0.8,  0.9],
            x5=[0.1,  0.2,  0.3,  0.4]))

@eg
def _ddiv4():
  ddv0(dict(x1=[101, 100, 99,   101,  99.5],
            x2=[101, 100, 99,   101, 100],
            x3=[101, 100, 99.5, 101,  99],
            x4=[101, 100, 99,   101, 100]))

@eg
def _ddiv5():
  ddv0(dict(x1=[11,11,11],
            x2=[11,11,11],
            x3=[11,11,11]))

@eg
def _ddiv6():
  ddv0(dict(x1=[11,11,11],
            x2=[11,11,11],
            x3=[32,33,34,35]))
    
def ddv0(data):
  for zz in ddiv(data):
    xx = zz["x"]
    yy = zz["y"]
    print("start  %.4f stop %.4f n %.4f" % (xx.lo, xx.hi, xx.n),end=" ")
    print("median %.4f mode %.4f has %s" % (xx.median(), yy.median(), len(zz["has"])),end= " ")
    print("has %s" % [s[0].label for s in zz["has"]])

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

