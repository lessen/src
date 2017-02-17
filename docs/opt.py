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


"""

# Easier Command-Line Options

Documentation for this code is available
[on-line](http://tttv1.net/GLOBALS.py).

## Synopsis

Install via `wget -O options.py http://ttvi1.net/GLOBALS.py`. Then use as follows:

     from opt import *
     # 
     our = options( 
       "1 line header",
       "Preamble text (multi-line).",
       "End text (multi-line).",
       group1 = [
         "1 line group description",
          ,h("1 line help",keyword1 = num")       # "--keyword1 X" expects any float
          ,h("1 line help",keyword2 = False")     # "--keyword2" will set keyword=True
          ,h("1 line help",keyword3 = str)        # "--keyword3 X" expects any string
          ,h("1 line help",keyword4 = [x,y,z..]") # "--keyword4 X" expects one of x,y,z...
                                                  # where the type of "X" is set from "x"
       ],
       group2 = [
         ...
       ])

After that, data on the above groups is stored in `our`; e.g. `our.group1.keyword1`.

## Description

The above call defines a variable `our` with fields (e.g.) 

     our.group1.keyword1

etc. Also, on the command line, 

     python codeThatUsesOptions.py--keyword1 X --keyword2 Y
     
will override the defaults shown below. Further, 

     python --help
     
will print help text, divided into the groups.
          
## Installation

    wget -O options.py http://tiny.cc/ttv1options

## How it Works

The standard way to process options in Python is the `argparse`
library which can be verbose, to say the least.  So this code is
an expansion function that takes a simple declarative syntax of the
optopms, then expands it into the argparse commands.

There's two functions that handle this process:

- `our=options(about,header,footer, groups)` writes a dictionary of options to `our`,
  while first checking if any command-line options overrides the defaults.
- `h(help,key=default)` is for one item. It exapnds into a whole
  dictionary of options for argparse.

Here are some examples of this expansions. For example,

       h("disable all tests", brave = False)

expands into

      dict(help    = "disable all test",
           key     = "--brave",
           default = False,
           action  = "store_true")

and

      h("split redos", splitRedo  = 20)

exapnds into

     dict(metavar = "S",
          key     = "--when",
          type    = str,
          choices = ["mon","tues","wed"],
          help    = "day of week",
          default = "mon"
         )

and 

      h("day of week", when=["mon","tues","wed"])

expands into

     dict(metavar = "S",
          key     = "--when",
          type    = str,
          choices = ["mon","tues","wed"],
          help    = "day of week",
          default = "mon"
         )

In the above `"mon"` was used as the default since it was
the first item in the when list.

"""

import sys,argparse

def h(help,**d):
  key,val = next(iter(d.items()))
  default = val[0] if isinstance(val,list) else val
  # step0: remember defaults
  out = dict(default=default)
  add = lambda **d : out.update(d) # convenience function for adding args
  # step1: Set type and meta var
  if   val is  not False:
    if   isinstance(default,int  ): add(metavar= "I", type= int)
    elif isinstance(default,float): add(metavar= "F", type= float)
    else                          : add(metavar= "S", type= str)
  # step2: add help and type-specific misc flags
  if   val is False :        add(help=help, action="store_true")
  elif isinstance(val,list): add(help=help, choices=val)
  else:                      add(help=help + ("; e.g. %s" % str(val)))
  # --------------
  return key, out

def options(prog, before, after, **d):
  class o:
    def __init__(i, **d)   : i.__dict__.update(d)
    def __repr__(i)        : return i.__dict__.__repr__()
    def __getitem__(i, k)  : return i.__dict__[k]
    def __setitem__(i,k,v) : i.__dict__[k] = v
  # -------------------------------
  parser = argparse.ArgumentParser(
               prog        = prog,
               description = before,
               epilog      = after,
               formatter_class=argparse.RawTextHelpFormatter)
  inside,out = {}, o()
  for context in sorted(d.keys()):
    out[context] = o()
    description = d[context][0]
    group = parser.add_argument_group(context, description)
    for key,rest in d[context][1:]:
      group.add_argument("--" + key,**rest)
      assert key not in inside, 'keys cannot repeat'
      inside[key] = context
  parsed = vars(parser.parse_args())
  for key,val in parsed.items():
    out[inside[key]][key]= val
  return out

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

