
from contextlib import contextmanager

def when(x,**d): return (x,d)

@contextmanager
def rx(klass,**d):
  b4 = {k: getattr(klass,k) for k in d}
  for k in d:
    setattr(klass,k,d[k])
  try:
    yield
  finally:
    for k in b4:
      setattr(klass,k,b4[k])


