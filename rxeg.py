from eg import eg
from rx import rx

@eg
def _rx():
  "Check the gizmo for temporarily changing class vars."
  class silly:
    X=1
    Y=min
  show=lambda s: print(s,dict(X=silly.X, Y=silly.Y.__name__))
  show("before")
  assert silly.X == 1
  with rx(silly,X=2,Y=max):
    show("inside")
    assert silly.X == 2
  show("after")
  assert silly.X == 1
