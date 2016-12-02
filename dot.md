[home](http://bit.ly/lessons) |
[copyright](https://github.com/lessen/src/blob/master/LICENSE.md) &copy;2016, tim&commat;menzies.us
<br>
[<img width=900 src="https://github.com/lessen/src/blob/master/img/banner.png?raw=true">](http://bit.ly/lessons)<br>
[src](https://github.com/lessen/src) |
[chat](https://lessons.slack.com/)

______

_(This file is auto-generated from [dot](dot).)_  

# Dot

Dot: ultra-portable config files  (for Unix tools on Mac and Linux)
Copyright (c) 2016, Tim Menzies tim@menzies.us, [MIT license v2](http://bit.ly/lessenlicense).

## Synopsis

    sh dot

## Description

When working on multiple machines, it is tedious to reconfigure each new
machine. Also, its bad manners to reconfigure someone else's machine unless
you undo it all when you leave.

Enter `dot`. This is a bash init file that sets up an new shell and writes
your preferred config files to `/tmp/$USER`.  
This current version of `dot` handles configs for 

- bash : numerous command-line tricks;
- github: quicker work flow 
     - `old` pulls from master; `new` commits and pushes to master
     - A tmp password server is enabled (so you only need to type
      your password every hour);
- emacs :
     - all emacs packages auto-downloaded and installed
     - cool packages are installed (ido, neotree, recent files, powerline)
     - mouse enabled, syntax highlighting enabled, etc
     - cool themes enabled
- vim :
     - Vim package manager installed
     - Line numbers enabled as is file path and title in header.
     - Incremebtal search enabled.
     - And other stuff besides
     - Note: don't have a good way to share the local spelling dictionary. Suggestions anyone?
- python 
     - adding sub-directories to PYTHONPATH and
     - disabling genration of those .pyc files.

Inside the dot shell, certain
standard commands are rewritten such that, when they are called, they use
config files written into `/tmp/$USER`.  Also, at start up, `dot` will perform
certain standard startup actions (initializes and/or downloads emacs packages).


The point of all this is that

1. All the code for `dot` is in one file, so easy to download.
2. When the `dot` shell exists, all that configs
   disappears. So no residual configurations.

## Installation

```sh
    wget -O dot http://bit.ly/timdot       # Code
    wget -O dot.md http://bit.ly/timdotdoc # Optional. Documentation.
    sh dot  
    dot0    # needed to install vim, emacs plugins.  only needs to be runs one
```
 
Note that the above `dot0` commands sometimes prints an ignorable error message
`window too small for splitting`.
