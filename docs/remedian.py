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
<br>
<script>
    (function() {
    var cx = '009630129455493240085:aja5uvdnjeo';
    var gcse = document.createElement('script'); gcse.type = 'text/javascript'; gcse.async = true;
    gcse.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') + '//www.google.com/cse/cse.js?cx=' + cx;
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(gcse, s);
})();
</script>
<div style="width:0px;overflow:hidden;height:0px;"> <!-- if you use display:none here, it doesn't work-->
    <gcse:search></gcse:search>
</div>
<form style="margin-left: 20px;" id="searchbox_009630129455493240085:aja5uvdnjeo" action="">
    <input value="009630129455493240085:aja5uvdnjeo" name="cx" type="hidden"/>
    <input value="FORID:11" name="cof" type="hidden"/>
    <input id="q" style=""  name="q" size="25" type="text"/>
    <button class="btn">Search</button>
</form>


<br clear=all>

_________________


Watch over a stream of numbers, incrementally learning their median.

Implemented via nested lists. New numbers are added to `lst[i]` and
when it fills up, it posts its median to `lst[i+1]`. Wen `lst[i+1]`
fills up, it posts the medians of its medians to `lst[i+2]`. Etc.
When a remedian is queried for the current median, it returns the
median of the last list with any numbers.

This approach is quite space efficient . E.g. four nested lists,
each with 64 items, require memory for 4*64 items yet can hold the
median of the median of the median of the median of over 17 million
numbers.

Example usage:

        z=remedian()
        for i in range(1000):
          z + i
          if not i % 100:
            print(i, z.median())

Based on  [The Remedian:A Robust Averaging Method for Large Data
Sets](http://web.ipac.caltech.edu/staff/fmasci/home/astro_refs/Remedian.pdf).
by Peter J. Rousseeuw and Gilbert W. Bassett Jr.  Journal of the
American Statistical Association March 1990, Vol. 85, No. 409,
Theory and Methods

The code [remedianeg.py](remedianeg.py) compares this rig to just
using Python's built-in sort then reporing the middle number.
Assuming lists of length 64 and use of pypy3:

- Remedian is getting nearly as fast (within 20%) as raw sort after 500 items;
- While at the same time, avoids having to store all the numbers in RAM;
- Further, remedian's computed median is within 1% (or less) of the medians found via Python's sort.

_____
## Programmer's Guide
"""
from median import median

class remedian:

  # Initialization
  def __init__(i,inits=[], k=64, # after some experimentation, 64 works ok
               about = None):
    i.all,i.k = [],k
    i.more,i._median=None,None
    [i + x for x in inits]

  # When full, push the median of current values to next list, then reset.
  def __add__(i,x):
    i._median = None
    i.all.append(x)
    if len(i.all) == i.k:
      i.more = i.more or remedian(k=i.k)
      i.more + i._medianPrim(i.all)
      i.all = []  # reset

  #  If there is a next list, ask its median. Else, work it out locally.
  def median(i):
    return i.more.median() if i.more else i._medianPrim(i.all)

  # Only recompute median if we do not know it already.
  def _medianPrim(i,all):
    if i._median == None:
      i._median = median(all,ordered=False)
    return i._median
 

"""
____


<img align=right 
src="https://raw.githubusercontent.com/timm/timm.github.io/master/timm.png"
width=170>
## Copyleft

Copyright &copy; 2016,2017 Tim Menzies <tim@menzies.us>, MIT license v2.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject
to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Share and enjoy.

"""

