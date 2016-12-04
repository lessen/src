from opt import *

our = options(
  "python smore.py",
  """
Timm Tools: misc python methods (data mining, optimization).
(C) 2016,2017 Tim Menzies, George Mathews MIT, v2.
The stuff we can use is either simple, or not at all.""",
  "",
  all=[
    "Misc options."
    ,h("disable all tests",        brave=    False)
    ,h("found for flags",          rounding= 3)
    ,h("verbose level (0=silent)", verbose=  [0,1,2,3])
  ],
  sample=[
    "Incrementally sample data."
    ,h("samples per column", samples= 256)
    ,h("small effect (Cliff's delta)", smallEffect= [0.147, 0.33, 0.474][0])
  ],
  num=[
    "Numeric samples."
    ,h("never normalize", noNorms= False)
  ],
  sym=[
    "Samples of symbols."
    ,h("bayesian k", k= 1)
    ,h("bayesian m", m= 2)
  ],
  groups=[
    "Groupings of distance"
    ,h("distance power",      f          = 2)
    ,h("distance columns",    cols       = ["objs","decs"])
    ,h("cull factor",         cull       = 0.5)
    ,h("smallest group size", minGroup   = 30)
    ,h("split redos",         splitRedo  = 20)  
    ,h("split bigger",        splitBigger= 0.1)        
  ]
)

if __name__ == "__main__":
  print("cull",our.groups.cull)
  print("verbose",our.all.verbose)
  print(our.all)
