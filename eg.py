# eg.py
# =====
#
# A very simple test engine inspired by Kent Beck's video: https://goo.gl/0bCy0X.
# Copyright (C) 2016, Tim Menzies BSD (2 clause).
#
# Usage
# -----    
#
# 1. Write many functions, each contain zero or more asserts.
# 2. Preface each such function with `@eg`
# 3. End file with `eg()`.
# 4. After that, then loading the file will run the examples.
#      -  This code catches any fails executions and, for each one, adds one to a
#         `FAIL` counter. Them at the end of the file, it reports the number of
#         functions that do not `FAIL`.
#      -  If a function contains a doco string, then that is printed before each
#         function is run.
#
# Example
#
#     # file = egdemo1.py
#     from eg import eg
#
#     @eg
#     def lstTest():
#       a={}
#       a[1]=10
#       assert a[1] == 10
#
#     # Other example functions here
#     
#     eg()
#
# Tips
# ----
#
# - `python egdemo1.py` will run all examples
# - `python egdemo1.py -?` will list all examples in the file.
# - `python egdemo1.py` -- a b c` will run just the examples `a`, `b` etc
#
# When I use this, then my code file file x.py has demos in (say) xeg.py whose
# first few lines are:
#
#        import x
#        from eg import eg
#
# To do
# -----
#
# Find some what to hook this into some continuous integration testing tool
# like https://travis-ci.org/.
#
# ___________________________________________________________________________

import traceback,re,random,sys,time

def eg(f=None, lst=[], seed=1):
  def doc(f):
    "Print function doco"
    if f.__doc__:
      print(re.sub(r'\n[ \t]*',"\n# ",f.__doc__))
  def some(lst):
    "Return just the examples mentioned on the command line"
    pairs = {f.__name__:f  for f in lst}
    return [pairs[x] for x in sys.argv if x  in pairs]
  def listAvailableExamples(lst):
    "For all items in lst, print their doc string"
    print("")
    for f in lst:
      print("%10s : " % f.__name__,end="")
      doc(f)
    print("")
  def run1(f):
    "Time the running of 1 function, print its doco string (if it has it)"
    hdr = "\n-----| %s |"+ ("-"*40)
    print(hdr % f.__name__,end="\n# ")
    doc(f)
    print("")
    t1=time.process_time()
    f()
    t2=time.process_time()
    print("# pass","(%.4f secs)" % (t2-t1))
  def runall(lst):
    "Run all the functions in lst, catching and counting all failures"
    if not lst:
      print("# No known examples.")
    else:
      PASS=FAIL=0
      random.seed(seed) 
      for f in lst:
        try:
          run1(f) 
          PASS += 1
        except Exception:
          print(traceback.format_exc())
          FAIL += 1
      print("\n## Test results: PASS = %s FAIL = %s %%PASS = %s"  % (
            PASS, FAIL, int(round(PASS*100/(PASS+FAIL+0.001)))))
  # -----------------------------------------------
  if   f                : lst += [f]
  elif "-?" in sys.argv : listAvailableExamples(lst)
  elif "--" in sys.argv : runall( some(lst) )
  else                  : runall( lst )
  return f


