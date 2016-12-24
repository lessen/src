from eg     import eg
from sample import sample
from random import seed

@eg
def _sample():
  seed(0)
  s=sample()
  for i in range(1000):
    s + i
    if i % 100 == 0: print(s,s.stats())
  s= sample(i for i in range(901))
  print(s,s.stats())

if __name__ == "__main__": eg()
