from sym import sym
from  eg  import eg
import re

words=""" 

You can do anything, but not everything.  
—David Allen

Perfection is achieved, not when there is nothing more to add, but when there is
nothing left to take away.
—Antoine de Saint-Exupéry

The richest man is not he who has the most, but he who needs the least.
—Unknown Author

You miss 100 percent of the shots you never take.  
—Wayne Gretzky

Courage is not the absence of fear, but rather the judgement that something else
is more important than fear.  
—Ambrose Redmoon

You must be the change you wish to see in the world.  
—Gandhi

When hungry, eat your rice; when tired, close your eyes. Fools may laugh at me,
but wise men will know what I mean.  
—Lin-Chi

The third-rate mind is only happy when it is thinking with the majority. The
second-rate mind is only happy when it is thinking with the minority. The
first-rate mind is only happy when it is thinking.  
—A. A. Milne

To the man who only has a hammer, everything he encounters begins to look like a
nail.  
—Abraham Maslow

We are what we repeatedly do; excellence, then, is not an act but a habit.
—Aristotle 

"""

words=re.sub(r'[-—,\.\n]'," ",words).split()

@eg
def _sym0():
  "Simple entropy calc."
  s= sym(["y"]*9 + ["n"] * 5)
  assert round(s.ent(),4)==0.9403
  
@eg
def _sym1():
  s= sym()
  for i,x in enumerate(words):
    s + x
    if i % 25 == 0: print(s)
  assert s.n == 199
  assert s.most == 13
  print(s)

@eg
def _sym2():
  s= sym( x for x in words )
  assert s.n == 199
  assert s.most == 13
  print(s)

if __name__ == "__main__" : eg()
