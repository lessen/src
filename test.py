import re,traceback
from choice import *

class ok:
  PASS = FAIL = 0
  BRAVE = our.all.tests

  @staticmethod
  def all():
    if our.all.tests:
      p,f = ok.PASS, ok.FAIL
      print("\n# PASS= %s FAIL= %s %%PASS = %s%%"  % (
            p, f, int(round(p*100/(p+f+0.001)))))
  def __init__(i,f):
    if not ok.brave:
      try:
        print("\n-----| %s |-----------------------" % f.__name__)
        if f.__doc__:
          print("# "+ re.sub(r'\n[ \t]*',"\n# ",f.__doc__))
        f()
        print("# pass")
        ok.PASS += 1
      except _:
        ok.FAIL += 1
        print(traceback.format_exc()) 
    return f

