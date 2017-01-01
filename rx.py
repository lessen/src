"""
Run some some experiments, setting some globals,
the un-doing those changes once the experiment fails.

Example:

      class silly:
        X=1
        Y=min
      class solly:
        Z=22
        B="love"
      def f1():
        return 3>1

      # begin experiments
      for _ in rx(solly, Z=[20,30], B=["love","hate"]):
        for _ in rx(  silly, X=[2,3], Y=[max,f1]):
          # insert your experiment here
          assert silly.X != 1
          assert solly.Z != 22

      # afterwards, we are back to the old values.
      assert silly.X == 1
      assert solly.Z == 22

______
## Programmer's Guide

In the following,  `klass` is some with attributes `k.v1,k.v2,..` etc
which we want to (temporarily) set 
to something else (and the something else comes from
the values in the dictionary `**d`). 

Note that the
values in `d` can be lists or a single items

"""

import itertools,sys

def rx(klass,**d):
  lst = [[(k,v) for v in
          # Ensure k's value is something we can iterate over. 
          (vs if type(vs)==list else [vs])] 
           for k,vs in d.items()]
  # Generate all combinations.
  combos = list( itertools.product(*lst) )
  # Run over the combinations.
  for settings in combos:
    now = {k:v for k,v in settings}
    # Cache the old settings.
    saved = {k:getattr(klass,k) for k in now}
    # Impose the temp settings.
    for k in now:
      setattr(klass,k,now[k])
    # Let something do something with the temp settings.
    yield now
    # Reset to old.
    for k in saved:
      setattr(klass,k,saved[k])


def rx1(lst):
  d   = {key:val for d in lst for key,val in d.items()}
  tmp = []
  for k,v in d.items():
    i = 1
    key = k[:i]
    while key in tmp and len(key) < len(k):
      i += 1
      key = k[:i]
    if   v==True       : v="1"
    elif v==False      : v="0"
    elif type(v)==float: v= "%g" % v
    elif type(v)==int  : v=v
    elif v.__class__.__name__ == 'function': v=v.__name__
    tmp += ["%s%s" % (key,v)]
  return ':'.join(tmp)

def say(*lst):
  print(*lst, sep=' ', end='', file=sys.stdout, flush=True)
        
      
      
