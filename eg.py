"""
`eg` is a very simple test engine inspired by [Kent Beck's maker
video](https://goo.gl/0bCy0X).

For every file `X.py` you want to show off, write a helper file `Xeg.py` whose
_last_ line is `eg()` and whose _first_ lines are

        import X
        from eg import eg

In the middle of `Xeg.py`, for every example you want to demonstrate, write one
functions, containing zero or more asserts.  Preface each such function with
`@eg`. For example:


       import X          # get the code you want to test
       from eg import eg # get this test engine
        
       @eg
       def lstTest():
         a={}
         a[1]=10
         assert a[1] == 10
        
       # Other example functions here
        
       # Finally
       if __name__ == '__main__': eg()

After that:

- `python Xeg.py` will run all examples
- `python Xeg.py -?` will list all examples in the file.
- `python Xeg.py -- a b c ` will run just the examples `a,b,c`.

Note that this code catches any fails executions and, for each one, adds one to
a `FAIL` counter. Them at the end of the file, it reports the number of
functions that do not `FAIL`.

Also, if a function contains a doc string, then that is printed before each
function is run. Further, the time to run each example function is displayed
on the screen.

Note that this code complains if ever it sees two examples with the same name.
Also, this code never runs the same example more than once.

### To do

Find some what to hook this into some continuous integration testing tool
like https://travis-ci.org/.

_____
## Programmer's Guide
"""

import traceback,re,random,sys,time

# This code resets the random number seed to `seed` before
# running any examples.
#
# Two default mutable arguments (`lst` and `runs`)
# are used as the working memory for this test engine:
# `lst` holds the list of example functions that might be executed;
# `runs` holds counts of how often each example function has been run
# (and this code ensures that function is never executed multiple times).
#
def eg(f=None, seed=1, lst=[], runs={} ):

  # ### Controlling the runs

  # Run one function `f`, print any output, plus its
  # runtime and the functions's name and doc string (if it exists).
  # Called by `runall`.
  def run1(f):
    runs[f.__name__] += 1 # if never run before, this value is now "1".
    if runs[f.__name__] == 1:  # only ever run once.
      hdr = "\n-----| %s |"+ ("-"*40)
      print(hdr % f.__name__,end="\n# ")
      doc(f)
      print("")
      t1=time.process_time()
      f()
      t2=time.process_time()
      print("# pass","(%.4f secs)" % (t2-t1))

  # Run all the functions in `examples`, catching and counting all failures.
  def runall(examples):
    if not examples:
      print("# No known examples.")
    else:
      PASS=FAIL=0
      random.seed(seed) # Reset the random seed before starting a demo.
      for f in examples:
        if runs[f.__name__] > 1: 
          continue
        try: # - Run via `try:except:` (so we can contie after crashes)
          run1(f) 
          PASS += 1 # If a function terminates correctly, increment `PASS`.
        except Exception:
          FAIL += 1 # If a crash, increment `FAIL`.
          print(traceback.format_exc())
      print("\n## Test results: PASS = %s FAIL = %s %%PASS = %s"  % (
            PASS, FAIL, int(round(PASS*100/(PASS+FAIL+0.001)))))


  # _______
  # ### Misc helper functions

  # Print function doco, it it has any. 
  #  It a multi-line string, print the lines left justified.
  def doc(f):
    if f.__doc__:
      print(re.sub(r'\n[ \t]*',"\n# ",f.__doc__))

  # Return just the examples mentioned on the command line.
  def some(lst):
    pairs = {f.__name__:f  for f in lst}
    return [pairs[x] for x in sys.argv if x  in pairs]

  # For all items in lst, print their doc string.
  def listAvailableExamples(lst):
    print("")
    for f in lst:
      print("%10s : " % f.__name__,end="")
      doc(f)
    print("")

  # _____
  # ### Run the script

  # If called as a decorator, add the function to the list of known functions.
  if f : 
    assert not f.__name__ in runs,("repeated test name %s" % f.__name__)
    runs[f.__name__] = 0
    lst += [f]
  # Else if called with the command line `python Xeg.py -?`,
  # it lists all the known functions, and their
  # documentation strings, in the file `Xeg.py`.
  elif "-?" in sys.argv : 
      listAvailableExamples(lst)
  # Else if called with the command line `python Xeg.py -- f1 f2 etc`,
  # it runs just the functions `f1,f2,etc` from the list of known functions.
  elif "--" in sys.argv : 
        runall( some(lst) )
  # Otherwise, it runs everything in the list of known functions.
  else : 
      runall( lst )
  return f # `eg` might be a decorator. So return function `f`.
