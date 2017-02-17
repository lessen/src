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


from csv import csv
from eg  import eg

@eg
def _csvFromString():
   "demo of read from string..."
   stringOfData="""a,b,
   c,d
   1,2.0,3,x
   10,20,30,y"""
   for row in csv(stringOfData, header=True):
      print(row)
   print(row)
   assert row == [10, 20.0, 30, 'y']

@eg
def _csvFromSimpleFile():
  "Reading a few Ascii rows."
  for row in csv(file="data/weather.csv"):
    print(row)
  
  assert row == ['rainy', 71.0, 'TRUE', 'no']

@eg
def _csvFromLargeFile(n=0):
    "Reading over 50MB+ of data."
    print("\nPlz wait a few seconds while I read 100MB+ of data...")
    for row in csv(file="data/weatherLarge.csv"):
      n +=1
    print(n,row)
    assert row == ['rainy', 71.0, 'TRUE', 'no']
    assert n == 1835009

@eg
def _csvFromZip(n=0):
    "Reading over 50MB of data."
    for row in csv(file="weatherLarge.csv",
                      zip="data/data.zip"):
      n += 1
      
    assert row == ['rainy', 71.0,  91,'TRUE', 'no']
    assert n == 1835009
    
if __name__ == "__main__": eg()

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

