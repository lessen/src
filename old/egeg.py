from eg import *

@ok
def  eg1():
  "checks for failing test"
  assert 1==2

@ok
def eg2():
  """checks for passing test. should
   run even if the above fails"""
  assert 1==1


oks()
