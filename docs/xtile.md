
# xtile

`xtile` summarizes a list of numbers as a list of percentiles,
then a little horizontal tile chart. Can show 1,000,000s of numbers in a single line.
 For example:

        from xtile import xtile
        
        tiles, nums, table = xtile(r() for _ in range(1000))
        print("pretty",tiles,table)
        print("raw   ",nums)
        
        pretty |   --------        *       --------   | 0.105, 0.317, 0.521, 0.719, 0.905
        raw    [0.105, 0.317, 0.521, 0.719, 0.905]

Note `xtile` returns three things: the tile's chart, the nums in
at the percentile breaks (all neatly justified) and the raw nums in a list
if case you need them for some other purpose.

### Xtiles

`xtiles` summarizes a list of lists of pairs of labels and numbers
and present them in tile charts using the same horizontal
scale for all numbers. For example:

        from xtile  import xtile, xtiles
        from random import random as r
        
        n = 100000
        s1= "s1",[r()**4/2      for _ in range(n)]
        s2= "s2",[r()**2        for _ in range(n)]
        s3= "s3",[r()**0.5*1.5  for _ in range(n)]
        s4= "s4",[r()**0.5*0.33 for _ in range(n)]
        for (a,b,c),d in xtiles([s1,s2,s3,s4]):
          print(a,c,":",d)
        
        # output:
        *  -----     |                           0.000, 0.004, 0.031, 0.120, 0.330 : s1
        | --  *-|                                0.104, 0.181, 0.234, 0.276, 0.313 : s4
        |-    *      --------     |              0.010, 0.090, 0.251, 0.492, 0.811 : s2
        |           ---------       *    ----  | 0.474, 0.819, 1.061, 1.256, 1.422 : s3


```python

def xtiles(pairs, width=40,rnd=3,sigs=4,
           ntiles=5 # legal values are 4 or 5
         ):
  pairs = [(name,sorted(lst)) for name,lst in pairs]
  lo   = sorted(map(lambda z:z[1][ 0], pairs))[0]
  up   = sorted(map(lambda z:z[1][-1], pairs))[-1]
  mid  = 2 if ntiles==5 else 1
  pairs= [ (xtile(pair[1],lo=lo,up=up,width=width,rnd=rnd,sigs=sigs,ntiles=ntiles),
            pair[0])
           for pair in pairs]
  return sorted(pairs,
                key = lambda z:z[0][1][mid])

The `xtile` utility.
def xtile(lst,lo=None, up=None,rnd=3,ntiles=5,width=40,sigs=4):
  lst = sorted(lst)
  lo   = lst[0]  if lo is None else lo
  up   = lst[-1] if up is None else up
  ros  = lambda lst: [int(x) if rnd==0 else round(x,rnd)
                      for x in lst]
  r    = lambda n: int(n)         # round
  ok   = lambda z: max(0, min(len(lst) - 1, z))
  yth  = lambda y: lst[ ok(r(len(lst)*y)) ]  # yth percentile item
  pos  = lambda y: r((yth(y) - lo) / (up - lo + 0.00001) * width) # xth place   
  tiles= [" "] * width
  seen = []
  if ntiles==5:
    for z in range(pos(0.1), pos(0.3)): tiles[z] = "-"
    for z in range(pos(0.7), pos(0.9)): tiles[z] = "-"
    seen = [yth(z) for z in [0.1,0.3,0.5,0.7,0.9]]
  else:
    for z in range(pos(0.25), pos(0.75)): tiles[z] = "-"
    seen = [pos(z) for z in [0.25,0.5,0.75]]
  tiles[ pos(0) ] = "|"
  tiles[ pos(1) ] = "|"
  tiles[ pos(0.5) ] = "*"
  f="%%%s.%sf" % (sigs,rnd)
  return ''.join(tiles), ros(seen), ', '.join([f % n for n in seen])

```

