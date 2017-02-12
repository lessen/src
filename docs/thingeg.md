
# thingeg

from eg     import eg
from thing  import thing
from random import seed

@eg
def _thing():
  seed(0)
  # nums
  t=thing()
  for i in range(1000):
    t + i
    if i % 100 == 0: print(t,t.samples.stats())
  t= thing(i for i in range(901))
  print(t,t.samples.stats())
  assert t.samples.stats()==(480.5,443)

  # symbols
  t= thing()
  for i in list("""Science is a way of thinking much more than it is a body of knowledge"""):
    t + i
  assert t.my.most==14
  
if __name__ == "__main__": eg()
```

