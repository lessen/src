import re,traceback
from GLOBALS import our

class eg:
  PASS = FAIL = 0
  enabled = not our.all.brave

def oks():
  if eg.enabled:
    p,f = eg.PASS, eg.FAIL
    print("\n# PASS= %s FAIL= %s %%PASS = %s%%"  % (
      p, f, int(round(p*100/(p+f+0.001)))))

def ok(f):
  if eg.enabled:
    try:
      print("\n-----| %s |-----------------------" % f.__name__)
      if f.__doc__:
        print("# "+ re.sub(r'\n[ \t]*',"\n# ",f.__doc__))
      f()
      print("# pass")
      eg.PASS += 1
    except Exception:
      eg.FAIL += 1
      print(traceback.format_exc()) 
  return f

