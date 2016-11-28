[home](http://bit.ly/lessons) |
[copyright](https://github.com/lessen/src/blob/master/LICENSE.md) &copy;2016, tim&commat;menzies.us
<br>
[<img width=900 src="https://github.com/lessen/src/blob/master/img/banner.png?raw=true">](http://bit.ly/lessons)<br>
[src](https://github.com/lessen/src) |
[chat](https://lessons.slack.com/)


______

# Dot

Dot: ultra-portable config files    
Copyright (c) 2016, Tim Menzies tim@menzies.us, [MIT license v2](http://bit.ly/lessenlicense).

## Synopsis

    sh dot

## Description

When working on multiple machines, it is tedious to reconfigure each new
machine. Also, its bad manners to reconfigure someone else's machine unless
you undo it all when you leave.

Enter `dot`. This is a bash init file that sets up an new shell and writes
your preferred config files to `/tmp/$USER`.  Inside the shell, certain
standard commands are rewritten such that, when they are called, they use
config files written into `/tmp/$USER`.  Also, at start up, `dot` will perform
certain standard startup actions (initializes and/or downloads emacs packages).

The point of all this is that

1. All the code for `dot` is in one file, so easy to download.
2. When the `dot` shell exists, all that configs
   disappears. So no residual configurations.

## Installation

    wget -O dot http://bit.ly/timdot       # Code
    wget -O dot.md http://bit.ly/timdotdoc # Optional. Documentation.

