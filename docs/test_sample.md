
# test_sample

import os

def ttv1egs(l,g):
  _, _, filenames =  next(iter(os.walk(".")))
  [__import__(x[:-3] ,l,g)
          for x in filenames 
          if x[-5:] == "eg.py"]

ttv1egs(locals(),globals)

from eg import eg

import egeg
import symeg
import numeg
import sampleeg
import thingeg
import remedianeg
import cliffsDeltaeg
import csveg
import statseg
import rangeseg

eg()
```

