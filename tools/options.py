
"""

# Easier Command-Line Options

## Synopsis

The following call defines a variable `THE` with fields (e.g.) 

     THE.group1.keyword1

etc. Also, on the command line, 

     python --keyword1 X --keyword2 Y
     
will override the defaults shown below. Further, 

     python --help
     
will print help text, divided into the groups.

     THE = options( 
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
     
## Installation

    wget -O options.py http://tiny.cc/ttv1options

## How it Works

The standard way to process options in Python is the `optparse`
library which can be verbose, to say the least.
So this code
is an expansion function that takes
a simple declarative syntax of the optopms, then
expands it into the optparse
commands. For example, this call:

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

(In the above `"mon"` was used as the default since it was
the first item in the when list.)

"""

import sys,argparse

def h(help,**d):
  key,val = d.items()[0]
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
  # step3: add "--" to key and return key and out
  return key, out

def options(prog, before, after, **d):
  """Convert dictionary 'd' to command line options
     divided into comand-line groups (one for every key
     in 'd'."""
  class o:
    def __init__(i, **d) : i.__dict__.update(d)
    def __repr__(i)      : return str(i.__dict__)

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




