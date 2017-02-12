import random

def more(x,y): return x > y
def less(x,y): return x < y

def rseed(s=None): random.seed(s or 1)
def r()          : return random.random()
def any(lst)     : return random.choice(lst)
def shuffle(lst) : random.shuffle(lst); return lst
```

