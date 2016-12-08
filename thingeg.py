from thing import thing
from eg import ok
from numbers import r

@ok
def _sdiv():
  th = thing([r() for _ in range(10000)])
  for segment in th.segments():
    print(segment)
    
