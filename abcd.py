"""

Watch over a classifier making predictions. As each prediction (and actual)
classification becomes available, send them to a logger class that incrementally
calculates accuracy, recall, false alarm rate, precision, f, g etc.

For example:

        a,b,c,d=list("abcd")
        log = abcd("data","rx")
        for want,got in [(a,b), (a,a), (a,c), (a,d), (b,a)]:
          log(want, got)
        log.report()

This prints
        
        # db                   rx            n    a    b   c   d    acc pd  pf  prec f  g  class
        ----------------------------------------------------------------------------------------------------
        # data                 rx            4    0    3   1    1   20  25 100  50  33   0 a
        # data                 rx            1    3    1   1    0   20   0  25   0  33   0 b
        # data                 rx            0    4    0   1    0   20   0  20   0  33   0 c
        # data                 rx            0    4    0   1    0   20   0  20   0  33   0 d
        ----------------------------------------------------------------------------------------------------
        # data                 rx            2    2    1   1    0   20  10  53  20  33   0

(The last line is the weighted sum of the column above it.)

If called from the command line, this code expects to read two words per line, for multiple lines.

- Line1 mentions the data and treatment applied.
- On all other lines, the words are first and section the actual and predicted values (respectively).

E.g.

        cat <<EOF | python3 abcd.py
        data rx
        a b
        a a
        a c
        a d
        b a

This prints out the same report as above.

_____
## Programmer's guide

"""
import sys,re


class abcd:

  # Initialize
  def __init__(i,db="all",rx="all"):
    i.db = db; i.rx=rx;
    i.yes = i.no = 0
    i.known = {}; i.a= {}; i.b= {}; i.c= {}; i.d={}

  # Incrementally update
  def __call__(i,actual=None,predict=None):
    i.knowns(actual)
    i.knowns(predict)
    if actual == predict: i.yes += 1 
    else                :  i.no += 1
    for x in  i.known:
      if actual == x:
        if  predict == actual: i.d[x] += 1 
        else                 : i.b[x] += 1
      else:
        if  predict == x     : i.c[x] += 1 
        else                 : i.a[x] += 1

  # Ensure we know class `x`. If `x` is new, then we have to back date
  # the "a" value (true negatives).
  def knowns(i,x):
    if not x in i.known:
      i.known[x]= i.a[x]= i.b[x]= i.c[x]=i.d[x]=0.0
    i.known[x] += 1
    if (i.known[x] == 1):
      i.a[x] = i.yes + i.no

  # Pretty print header
  def header(i):
    print("#",
        ('{0:20s} {1:11s}   {2:4s} {3:4s} {4:4s}'+\
        '{5:4s}{6:4s} {7:3s} {8:3s} {9:3s} '+ \
        '{10:3s} {11:3s}{12:3s}{13:10s}').format( 
        "db","rx","n","a","b","c","d","acc","pd",
        "pf","prec","f","g","class"))
    print('-'*100)

  # Computer the performance scores  
  def scores(i):
    class oo:
      def __init__(i, **adds):
        i.__dict__.update(adds)
    def p(y) : return int(100*y + 0.5)
    def n(y) : return int(y)
    out = {}
    
    for x in i.known:
      pd  = pf = pn = prec = g = f = acc = 0

      a = i.a[x]; b= i.b[x]; c= i.c[x]; d= i.d[x]
      
      if (b+d)    : pd   = d     / (b+d)
      if (a+c)    : pf   = c     / (a+c)
      if (a+c)    : pn   = (b+d) / (a+c)
      if (c+d)    : prec = d     / (c+d)
      if (1-pf+pd): g    = 2*(1-pf)*pd / (1-pf+pd)
      if (prec+pd): f    = 2*prec*pd/(prec+pd)
      if (i.yes + i.no): acc= i.yes/(i.yes+i.no)
      out[x] = oo(db=i.db, rx=i.rx, yes= n(b+d),
                  r = (c + d)/(i.yes + i.no),
                 all=n(a+b+c+d), a=n(a),
                 b=n(b), c=n(c), d=n(d), acc=p(acc), pd=p(pd),
                 pf=p(pf), prec=p(prec), f=p(f), g=p(g),x=x)
    return out

  # Write the performance scores for each class, then the
  # weighted sum of those scores across all classes.
  def report(i):
    i.header()
    db = rx = ""
    yes=a=b=c=d=acc=pd=pf=prec=f=g=0
    for x,s in sorted(i.scores().items()):
      print("#",
       ('{0:20s} {1:10s} {2:4d} {3:4d} {4:4d}'+\
        '{5:4d} {6:4d} {7:4d} {8:3d} {9:3d} '+ \
        '{10:3d} {11:3d} {12:3d} {13:10s}').format(
          s.db, s.rx,  s.yes, s.a, s.b, s.c, s.d, 
          s.acc, s.pd, s.pf, s.prec, s.f, s.g, x))
      a    += s.a    * s.r
      b    += s.b    * s.r
      c    += s.c    * s.r
      d    += s.d    * s.r
      acc  += s.acc  * s.r
      pd   += s.pd   * s.r
      pf   += s.pf   * s.r
      prec += s.prec * s.r
      f    += s.f    * s.r
      g    += s.g    * s.r
      yes  += s.yes  * s.r
      db,rx = s.db, s.rx
    print('-'*100)
    print("#",
       ('{0:20s} {1:10s} {2:4.0f} {3:4.0f} {4:4.0f}'+\
        '{5:4.0f} {6:4.0f} {7:4.0f} {8:3.0f} {9:3.0f} '+ \
        '{10:3.0f} {11:3.0f} {12:3.0f} {13:10s}').format(
          db,  rx,  yes, a, b, c, d, 
          acc, pd, pf, prec, f, g, ""))


# Tool for reading in the data from standard input.
if __name__ == "__main__":
  log = None
  for line in sys.stdin:
    words= re.sub(r"[\n\r]","",line).split(" ")
    one,two= words[0],words[1]
    if log:
      log(one,two)
    else:
      log=abcd(one,two)
  log.report()
      