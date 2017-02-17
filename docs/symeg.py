""" 
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-55634425-2', 'auto');
  ga('send', 'pageview');

</script>
<img 
src="https://avatars0.githubusercontent.com/u/23156192?v=3&s=200"
align=left
width=120>
&nbsp;<br>&nbsp;<br>
&nbsp;&nbsp; [home](http://ttv1.github.io) | [discuss](#discussion) | [report bug](https://github.com/ttv1/src/issues) 


<br clear=all>

_________________


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

"""
____


<img align=right 
src="https://raw.githubusercontent.com/timm/timm.github.io/master/timm.png"
width=170>
## Copyleft

Copyright &copy; 2016 Tim Menzies <tim@menzies.us>

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The F*ck You Want
To Public License, Version 2, as published by Sam Hocevar. See
[http://www.wtfpl.net](http://www.wtfpl.net) for more details.

Share and enjoy.

"""

