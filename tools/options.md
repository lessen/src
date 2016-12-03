[home](http://bit.ly/lessons) |
[copyright](https://github.com/lessen/src/blob/master/LICENSE.md) &copy;2016, tim&commat;menzies.us
<br>
[<img width=900 src="https://github.com/lessen/src/blob/master/img/banner.png?raw=true">](http://bit.ly/lessons)<br>
[src](https://github.com/lessen/src) |
[chat](https://lessons.slack.com/)

______

_(This file is auto-generated from [options.py](options.py).)_  



# Easier Command-Line Options

Documentation for this code is available [on-line](http://tiny.cc/ttv1optionsdoc).

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

