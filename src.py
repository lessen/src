"""

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
