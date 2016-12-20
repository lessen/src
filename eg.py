"""

Just another [Timm Tools](index.html).

____
## About

`eg` is a very simple test engine inspired by [Kent Beck's maker
video](https://goo.gl/0bCy0X).
    
### Usage

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
       eg()

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

### To do
    
Find some what to hook this into some continuous integration testing tool
like https://travis-ci.org/.

"""
# ____
# ## Programmer's Guide

import traceback,re,random,sys,time

def eg(f=None, lst=[], seed=1):
  """Top-level interface."""
  # ### Helper functions

  def runall(lst):
    """Run all the functions in lst, catching and counting all failures."""
    if not lst:
      print("# No known examples.")
    else:
      PASS=FAIL=0
      # - Always set the random seed before starting a demo.
      random.seed(seed) 
      for f in lst:
        # - Run inside a   `try:except:` so one crash does not stop the other examples running
        try:
          run1(f) 
          # If a function terminates correctly, increment `PASS`.
          PASS += 1
        except Exception:
          # If a crash, increment `FAIL`.
          FAIL += 1
          print(traceback.format_exc())
      # Report number of `PASS`es and `FAIL`s.
      print("\n## Test results: PASS = %s FAIL = %s %%PASS = %s"  % (
            PASS, FAIL, int(round(PASS*100/(PASS+FAIL+0.001)))))
  def run1(f):
    """
    Run one function `f`, print any output, plus its
    runtime and the functions's name. and doc string (if it exists).
    """
    hdr = "\n-----| %s |"+ ("-"*40)
    print(hdr % f.__name__,end="\n# ")
    doc(f)
    print("")
    t1=time.process_time()
    f()
    t2=time.process_time()
    print("# pass","(%.4f secs)" % (t2-t1))
  def doc(f):
    """
    Print function doco, it it has any. 
    It a multi-line string, print the lines left justified.
    """
    if f.__doc__:
      print(re.sub(r'\n[ \t]*',"\n# ",f.__doc__))
  def some(lst):
    """Return just the examples mentioned on the command line."""
    pairs = {f.__name__:f  for f in lst}
    return [pairs[x] for x in sys.argv if x  in pairs]
  def listAvailableExamples(lst):
    """For all items in lst, print their doc string."""
    print("")
    for f in lst:
      print("%10s : " % f.__name__,end="")
      doc(f)
    print("")
    
  # ### Run the script

  # If called as a decorator, add the function to the list of known functions.
  if f : lst += [f]
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
  return f 

  
"""
____
## Copyright

<img align=right src="http://poster.keepcalmandposters.com/1520904.png" width=170>
Copyright © 2016 Tim Menzies <tim@menzies.us>

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The F*ck You Want
To Public License, Version 2, as published by Sam Hocevar. See
[http://www.wtfpl.net](http://www.wtfpl.net) for more details. 

"""
