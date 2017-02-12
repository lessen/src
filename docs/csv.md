
# csv


- Can read from ascii files, zip files, or strings.
- Rows are `yield`ed one a time, so it is possible to
  use this code to incremental process very large files
  without first loading all file contents into ram.
- Knows to delete comments and whitespace.
- Allows rows on one line to the continued
  to the next line (which is done if the first line ends in `,`).
- Columns can contain missing  values (marked with a `?`).
- Column contents are converted into `int`s or `float`s or
  left as strings, as appropriate.
- If called with the default `header=True` flag, then the
  first row is returned verbatim.

`csv` is not slow.  For example, on one machine, with pypy3, `csv` can load
nearly two million records in under six seconds-- and even faster if that data
is read from a zip file.

### Examples

#### Template for standard usage

        from csv import csv
        #
        for row in csv(...):
           doSomething(row)

Can read from strings, files, zip files.

#### Example #1: from string

        from csv import csv
        #
        stringOfData="a,b,
        c,d
        1,2.0,3,x
        10,20,30,y"
        for row in csv(stringOfData, header=True):
           print(row)

#### Example #2: read from ascii file.

        from csv import csv
        #
        for row in csv(file="data/weather.csv"):
          print(row)


#### Example #3: read from zip file

        from csv import csv
        #
        for row in csv(file = "weatherLarge.csv",
                        zip  = "data/data.zip"):
          print(row)


```python

_____
## Programmer's Guide


import zipfile,re


def csv(str= None, file= None, zip= None, header= True,
         SEPERATOR = ",",
         MISSING   = "?",
         DOOMED     = '([\n\r\t]|#.*)'):

  # _____
  # ### Misc helpers

  # Convert strings to strings
  def string(x) : return x

  # Needed when reading zip files.
  def utf8(x) : return x.decode("utf-8") 

  """
  ______
  ### Generator: `yieldAllRow`

  The `rows` function kills whitespace and comments (i.e. all the
  things defined in `DOOMED`).  

  Also, it combines lines that end in `,` with the
  next line.  
 
  Further, it breaks up the lines into cells (dividing at the
  `SEPERATOR`).  

  After that, strings within cells are converted to their
  appropriate type (using `compileRow`).  

  Finally, the function complains if any
  row is a diofferent size to the first row.

  Todo: when there are headers, don't compile on cols that are marked as missing.
  """  
  def rows(src,n=0,rules=[], lines=[], filter=string):
   for line0 in src:
     line1 = filter(line0)
     line2 = re.sub(DOOMED, "", line1)
     if line2:
       lines += [line2]
       if line2[-1] != SEPERATOR:
         tmp   = ''.join(lines)
         lines = []
         row   = [z.strip() for z in tmp.split(",")]
         if len(row)> 0:
           n += 1
           if n==1:
             rules = [None] * len(row)
           else:
             assert len(row) == len(rules),("expected %s cells in this row" % len(rules))
           yield row if n==1 and header else compileRow(row,rules) #... 7

  """
  _________________________________
  ### Compile one row

  To `compileRow` we call `compileCell` on each item in the row.

  To `compileCell`, we need some `rules` that know how to convert strings into
  `int`s, `float`s, or just leave as `string`s.

  In `compileCell`, the first time we see something in a column that is not a MISSING value,
  we  ask `what2do` to work   out how to convert that thing into its proper type
  (this is done using some calls to `try:except:`).

  The results of  `what2do` are cached in `rules` so that,  after that first value,
  we know how to compile things in this column. Important note: without 
  that cache, this code is five to ten times slower to execute.

  """
  def compileRow(lst,rules):
    def what2do(x):
      try:  int(x); return int
      except ValueError:
        try:  float(x); return float
        except ValueError:
          return string
    def compileCell(i,x):
      if x != MISSING:
        rule = rules[i] = rules[i] or what2do(x)
        return rule(x)
      return x
    return [compileCell(i,cell)
             for i,cell in enumerate(lst)]

  # If the csv has headers, and if those headers
  # start with the `MISSING` marker, then just yield
  # the columns that are not `MISSING`. Otherwise,
  # just yield all rows.
  def cols(src):
    """Yields just the columns not marked as missing."""
    if header:
      use = []
      for row in src:
        use = use or [col for col,cell in enumerate(row)
                      if  cell[0] != MISSING ]
        yield [row[col] for col in use]
    else:
      for row in src:
        yield row
  """ 
______

### Main

  """
  # Read from zip
  if zip:
    with zipfile.ZipFile(zip, 'r') as myzip:
      with myzip.open(file) as src:
        for row in cols(rows( src, filter=utf8 )):
          yield row

  # Read from file
  elif file:
    with open(file) as src:
      for row in cols(rows( src )):
        yield row

  # Read from string
  elif str:
    for row in cols(rows( str.splitlines() )):
      yield row
```

