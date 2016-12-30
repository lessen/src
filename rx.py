from contextlib import contextmanager
import itertools

def rx(klass,**d):
  lst = [[(k,v) for v
          in (vs if type(vs)==list else [vs])]
           for k,vs in d.items()]
  lst = list( itertools.product(*lst) )
  for settings in lst:
    d = {k:v for k,v in settings}
    with rx1(klass,d):
      yield d
  
@contextmanager
def rx1(klass, d):
  b4 = {k: getattr(klass,k) for k in d}
  for k in d:
    setattr(klass,k,d[k])
  try:
    yield
  finally:
    for k in b4:
      setattr(klass,k,b4[k])
