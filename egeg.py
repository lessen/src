from eg import eg

@eg
def _passes1():
  "Check the test engine recognizes a 'pass'."
  assert 1==1


@eg
def _failes():
  "Check the test engine recognizes a 'fail'."
  assert 1==2, 'this should fail'


@eg
def _passes2():
  "Check that even after a fail, other functions get called."
  assert 10==10

eg() 
