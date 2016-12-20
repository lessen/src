   
import traceback,re,random,sys,time

def eg(f=None, lst=[], seed=1):
    """
    A very simple test engine inspired by [Kent Beck's maker video](https://goo.gl/0bCy0X).   
    Copyright (C) 2016, Tim Menzies BSD (2 clause).
    
    ## Usage
    
    1. Write many functions, each contain zero or more asserts.
    2. Preface each such function with `@eg`
    3. End file with `eg()`.
    4. After that, then loading the file will run the examples.
         -  This code catches any fails executions and, for each one, adds one to a
            `FAIL` counter. Them at the end of the file, it reports the number of
            functions that do not `FAIL`.
         -  If a function contains a doco string, then that is printed before each
            function is run.
    
    ## Example
    
        # file = egdemo1.py
        from eg import eg
    
        @eg
        def lstTest():
          a={}
          a[1]=10
          assert a[1] == 10
    
        # Other example functions here
        
        eg()
    
    ## Tips
    
    - `python egdemo1.py` will run all examples
    - `python egdemo1.py -?` will list all examples in the file.
    - `python egdemo1.py` -- a b c ` will run just the examples `a`, `b` etc
    
    When I use this, then my code file file x.py has demos in (say) xeg.py whose
    first few lines are:
    
           import x
           from eg import eg
    
    ## To do
    
    Find some what to hook this into some continuous integration testing tool
    like https://travis-ci.org/.

    ______

    ## Helper Functions
  """
  def runall(lst):
    # Run all the functions in lst, catching and counting all failures.
    if not lst:
      print("# No known examples.")
    else:
      PASS=FAIL=0
      # - Always set the random seed before starting a demo.
      random.seed(seed) 
      for f in lst:
        # - Run inside a   `try:except:` so on crash does not stop the other examples running
        try:
          run1(f) 
          PASS += 1
        except Exception:
          # If a crash, increment `FAIL`.
          FAIL += 1
          print(traceback.format_exc())
      print("\n## Test results: PASS = %s FAIL = %s %%PASS = %s"  % (
            PASS, FAIL, int(round(PASS*100/(PASS+FAIL+0.001)))))
  def run1(f):
    # Run some function `f`, print any output, plus its
    # runtime and the functions's name.
    hdr = "\n-----| %s |"+ ("-"*40)
    print(hdr % f.__name__,end="\n# ")
    doc(f)
    print("")
    t1=time.process_time()
    f()
    t2=time.process_time()
    print("# pass","(%.4f secs)" % (t2-t1))
  def doc(f):
    # Print function doco, it it has any. 
    # It a multi-line string, print the lines left justified.
    if f.__doc__:
      print(re.sub(r'\n[ \t]*',"\n# ",f.__doc__))
  def some(lst):
    # Return just the examples mentioned on the command line.
    pairs = {f.__name__:f  for f in lst}
    return [pairs[x] for x in sys.argv if x  in pairs]
  def listAvailableExamples(lst):
    # For all items in lst, print their doc string.
    print("")
    for f in lst:
      print("%10s : " % f.__name__,end="")
      doc(f)
    print("")
  # _____
  #
  # ## Main driver
  #
  # This code does different things, depending on how it is call.
  # If used as a decorator before some function `f`, that function is added to the lost of known functions.
  if f : lst += [f]
  # Else if called with the command line `python xxx.py -?`,
  # it lists all the known functions, and their
  # documentation strings, in the file `xxx.py`.
  elif "-?" in sys.argv : 
      listAvailableExamples(lst)
  # Else if called with the command line `python xxx.py -- f1 f2 etc`,
  # it runs just the functions `f1,f2,etc` from the list of known functions.
  elif "--" in sys.argv : 
        runall( some(lst) )
  # Otherwise, it runs everything in the list of known functions.
  else : 
      runall( lst )
  return f 


