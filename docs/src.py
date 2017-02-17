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



# Rules of src

## Optimizations

Best to run this with pypy3

## Using global options

Files needing global options start with `from choice import *`.

Global options are read into class static variables using, eg.


```
class num:
  hedges = our.num.hedges # 0.38
  conf   = our.num.conf   # 0.95
  
```

Thereafter, code needed the options talks to `className.var` and not
`our.x.y`. Why?  Well, if you are sick of my global system, then dump it and
make all the config static class variables.

Todo
====

- slit numeg over into thing

- redp div knowing abut thing.n()

"""
from GLOBALS import *
import sys,re
import GLOBALS
from pprint import pprint
from collections import defaultdict
from itertools import takewhile, count

def tsort(graph):
    levels_by_name = {}
    names_by_level = defaultdict(set)

    def walk_depth_first(name):
        if name in levels_by_name:
            return levels_by_name[name]
        children = graph.get(name, None)
        level = 0 if not children else (1 +
                      max(walk_depth_first(lname)
                          for lname in children))
        levels_by_name[name] = level
        names_by_level[level].add(name)
        return level

    for name in graph:
        walk_depth_first(name)

    return list(takewhile(lambda x: x is not None,
                          (names_by_level.get(i, None)
                           for i in count())))
  
graph = dict(eg     = ["GLOBALS"],
             GLOBALS= ["opt"],
             sample = ["GLOBALS"],
             num    = ["GLOBALS"],
             sym    = ["GLOBALS"],
             egeg   = ["eg"],
             table  = ["num","sym"])

if our.all.egs:
   import os
   files=[f for f in os.listdir('.') if re.match(r'.*eg\.py', f)]
   print(files)
   for file in files:
      if file == '__init__.py' : continue
      if file=="src.py"        : continue
      if file=="eg.py"         : continue
      print("########################")
      print("#",file)
      print("########################")
      __import__(file[:-3])
   oks()
   
if our.all.depends:
  pprint( tsort(graph))

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

