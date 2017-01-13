"""
Watch over a learner making numeric predictions.

"""

import sys,re

class nerror:
  def __init__(i, db="all",rx="rx"):
    i.db = str(db)
    i.log = []

  def __call__(i, actual=None,predict=None):
    i.log += [(actual,predict)]
    thing + mre

  def header(i):
    print("#"),
    '{0:20s} {1:11s}   {2:4s} {3:4s} {4:4s} {5:4s}{6:4s} '.format( 
        "db","rx","n","re","mre","sa","pred(25)","pred(50)")
    print('-'*100)

  def report  

