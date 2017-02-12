
# rxeg

from eg import eg
from rx import rx


@eg
def _rx():
  "Check the gizmo for temporarily changing class vars."
  class silly:
    X=1
    Y=min
  class solly:
    Z=22
    B="love"
  def f1():
    return 3>1
  n = 0
  for _ in rx(solly, Z=[20,30], B=["love","hate"]):
    for _ in rx(  silly, X=[2,3], Y=[max,f1]):
      print("sX", silly.X, "soZ",
            solly.Z,"f",silly.Y.__name__)
      n += 1 
      assert silly.X != 1
      assert solly.Z != 22
  assert silly.X == 1
  assert solly.Z == 22
  assert n == 16

eg()
```

