# eg.py
# =====
#
# A very, very simple test engine.
# Copyright (C) 2016, Tim Menzies BSD (2 clause)
#
# Usage
# -----
#
# 1. Write many functions, each contain zero or more asserts.
# 2. Preface each such function with `@eg`
# 3. End file with `eg()`.
#
# Example
#
#     @eg
#     def lstTest():
#       a={}
#       a[1]=10
#       assert a[1] == 10
#
#     # Other example functions here
#     
#     ok()
#
# Note
# ----
#
# -  This code catches any fails executions and, for each one, adds one to a
#    `FAIL` counter. Them at the end of the file, it reports the number of
#    functions that do not `FAIL`.
# -  If a function contains a doco string, then that is printed before each
#    function is run.
#
# ___________________________________________________________________________

import traceback,re,random

def eg(f=None,lst=[], # evil use a persistent list to cache the functions.
       seed=1):
  if f:
    lst += [f]
  else:
    random.seed(seed)
    PASS=FAIL=0
    for f in lst:
      try:
        print("\n-----| %s |-----------------------" % f.__name__)
        if f.__doc__:
          print("# "+ re.sub(r'\n[ \t]*',"\n# ",f.__doc__),"\n")
        f()
        print("# pass")
        PASS += 1
      except Exception:
        FAIL += 1
        print(traceback.format_exc())
    print("\n# PASS= %s FAIL= %s %%PASS = %s%%"  % (
          PASS, FAIL, int(round(PASS*100/(PASS+FAIL+0.001)))))
  return f

