from eg import eg
from abcd import abcd

@eg
def _abcd1():
  a,b,c,d=list("abcd")
  log = abcd("data","rx")
  for want,got in [(a,b), (a,a), (a,c), (a,d), (b,a)]:
    log(want, got)
  log.report()

if __name__ == "__main__": eg()
```

