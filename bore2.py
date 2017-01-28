import re

def X(_) : return "?"
def F(x) : return float(x)
def S(x) : return x
def I(x) : return int(x)

def nasa93():
  t = table(
  names=[
     "recordnumber", "projectname", "cat2", "forg", "center", "year", "mode", "rely",
     "data", "cplx", "time", "stor", "virt", "turn", "acap", "aexp", "pcap", "vexp",
     "lexp", "modp", "tool", "sced", "equivphyskloc", "#act_effort"],
  types=[
      X,S, S,                 S,I,I,   S,           S,S,S,S,S,S,S,S,S,S,S,S,S,S,S,F,   F])
  t.data([
    c("1,de,avionicsmonitoring,g,2,1979,semidetached,h,l,h,n,n,l,l,n,n,n,n,h,h,n,l,25.9,117.6"),
    c("2,de,avionicsmonitoring,g,2,1979,semidetached,h,l,h,n,n,l,l,n,n,n,n,h,h,n,l,24.6,117.6"),
    c("3,de,avionicsmonitoring,g,2,1979,semidetached,h,l,h,n,n,l,l,n,n,n,n,h,h,n,l,7.7,31.2"),
    c("4,de,avionicsmonitoring,g,2,1979,semidetached,h,l,h,n,n,l,l,n,n,n,n,h,h,n,l,8.2,36"),
    c("5,de,avionicsmonitoring,g,2,1979,semidetached,h,l,h,n,n,l,l,n,n,n,n,h,h,n,l,9.7,25.2"),
    c("6,de,avionicsmonitoring,g,2,1979,semidetached,h,l,h,n,n,l,l,n,n,n,n,h,h,n,l,2.2,8.4"),
    c("7,de,avionicsmonitoring,g,2,1979,semidetached,h,l,h,n,n,l,l,n,n,n,n,h,h,n,l,3.5,10.8"),
    c("8,erb,avionicsmonitoring,g,2,1982,semidetached,h,l,h,n,n,l,l,n,n,n,n,h,h,n,l,66.6,352.8"),
    c("9,gal,missionplanning,g,1,1980,semidetached,h,l,h,xh,xh,l,h,h,h,h,n,h,h,h,n,7.5,72"),
    c("10,gal,missionplanning,g,1,1980,semidetached,n,l,h,n,n,l,l,h,vh,vh,n,h,n,n,n,20,72"),
    c("11,gal,missionplanning,g,1,1984,semidetached,n,l,h,n,n,l,l,h,vh,h,n,h,n,n,n,6,24"),
    c("12,gal,missionplanning,g,1,1980,semidetached,n,l,h,n,n,l,l,h,vh,vh,n,h,n,n,n,100,360"),
    c("13,gal,missionplanning,g,1,1985,semidetached,n,l,h,n,n,l,l,h,vh,n,n,l,n,n,n,11.3,36"),
    c("14,gal,missionplanning,g,1,1980,semidetached,n,l,h,n,n,h,l,h,h,h,l,vl,n,n,n,100,215"),
    c("15,gal,missionplanning,g,1,1983,semidetached,n,l,h,n,n,l,l,h,vh,h,n,h,n,n,n,20,48"),
    c("16,gal,missionplanning,g,1,1982,semidetached,n,l,h,n,n,l,l,h,n,n,n,vl,n,n,n,100,360"),
    c("17,gal,missionplanning,g,1,1980,semidetached,n,l,h,n,xh,l,l,h,vh,vh,n,h,n,n,n,150,324"),
    c("18,gal,missionplanning,g,1,1984,semidetached,n,l,h,n,n,l,l,h,h,h,n,h,n,n,n,31.5,60"),
    c("19,gal,missionplanning,g,1,1983,semidetached,n,l,h,n,n,l,l,h,vh,h,n,h,n,n,n,15,48"),
    c("20,gal,missionplanning,g,1,1984,semidetached,n,l,h,n,xh,l,l,h,h,n,n,h,n,n,n,32.5,60"),
    c("21,X,avionicsmonitoring,g,2,1985,semidetached,h,l,h,n,n,l,l,n,n,n,n,h,h,n,l,19.7,60"),
    c("22,X,avionicsmonitoring,g,2,1985,semidetached,h,l,h,n,n,l,l,n,n,n,n,h,h,n,l,66.6,300"),
    c("23,X,simulation,g,2,1985,semidetached,h,l,h,n,n,l,l,n,n,n,n,h,h,n,l,29.5,120"),
    c("24,X,monitor_control,g,2,1986,semidetached,h,n,n,h,n,n,n,n,h,h,n,n,n,n,n,15,90"),
    c("25,X,monitor_control,g,2,1986,semidetached,h,n,h,n,n,n,n,n,h,h,n,n,n,n,n,38,210"),
    c("26,X,monitor_control,g,2,1986,semidetached,n,n,n,n,n,n,n,n,h,h,n,n,n,n,n,10,48"),
    c("27,X,realdataprocessing,g,2,1982,semidetached,n,vh,h,vh,vh,l,h,vh,h,n,l,h,vh,vh,l,15.4,70"),
    c("28,X,realdataprocessing,g,2,1982,semidetached,n,vh,h,vh,vh,l,h,vh,h,n,l,h,vh,vh,l,48.5,239"),
    c("29,X,realdataprocessing,g,2,1982,semidetached,n,vh,h,vh,vh,l,h,vh,h,n,l,h,vh,vh,l,16.3,82"),
    c("30,X,communications,g,2,1982,semidetached,n,vh,h,vh,vh,l,h,vh,h,n,l,h,vh,vh,l,12.8,62"),
    c("31,X,batchdataprocessing,g,2,1982,semidetached,n,vh,h,vh,vh,l,h,vh,h,n,l,h,vh,vh,l,32.6,170"),
    c("32,X,datacapture,g,2,1982,semidetached,n,vh,h,vh,vh,l,h,vh,h,n,l,h,vh,vh,l,35.5,192"),
    c("33,X,missionplanning,g,2,1985,semidetached,h,l,h,n,n,l,l,n,n,n,n,h,h,n,l,5.5,18"),
    c("34,X,avionicsmonitoring,g,2,1987,semidetached,h,l,h,n,n,l,l,n,n,n,n,h,h,n,l,10.4,50"),
    c("35,X,avionicsmonitoring,g,2,1987,semidetached,h,l,h,n,n,l,l,n,n,n,n,h,h,n,l,14,60"),
    c("36,X,monitor_control,g,2,1986,semidetached,h,n,h,n,n,n,n,n,n,n,n,n,n,n,n,6.5,42"),
    c("37,X,monitor_control,g,2,1986,semidetached,n,n,h,n,n,n,n,n,n,n,n,n,n,n,n,13,60"),
    c("38,X,monitor_control,g,2,1986,semidetached,n,n,h,n,n,n,n,n,n,h,n,h,h,h,n,90,444"),
    c("39,X,monitor_control,g,2,1986,semidetached,n,n,h,n,n,n,n,n,n,n,n,n,n,n,n,8,42"),
    c("40,X,monitor_control,g,2,1986,semidetached,n,n,h,h,n,n,n,n,n,n,n,n,n,n,n,16,114"),
    c("41,hst,datacapture,g,2,1980,semidetached,n,h,h,vh,h,l,h,h,n,h,l,h,h,n,l,177.9,1248"),
    c("42,slp,launchprocessing,g,6,1975,semidetached,h,l,h,n,n,l,l,n,n,h,n,n,h,vl,n,302,2400"),
    c("43,Y,application_ground,g,5,1982,semidetached,n,h,l,n,n,h,n,h,h,n,n,n,h,h,n,282.1,1368"),
    c("44,Y,application_ground,g,5,1982,semidetached,h,h,l,n,n,n,h,h,h,n,n,n,h,n,n,284.7,973"),
    c("45,Y,avionicsmonitoring,g,5,1982,semidetached,h,h,n,n,n,l,l,n,h,h,n,h,n,n,n,79,400"),
    c("46,Y,avionicsmonitoring,g,5,1977,semidetached,l,n,n,n,n,l,l,h,h,vh,n,h,l,l,h,423,2400"),
    c("47,Y,missionplanning,g,5,1977,semidetached,n,n,n,n,n,l,n,h,vh,vh,l,h,h,n,n,190,420"),
    c("48,Y,missionplanning,g,5,1984,semidetached,n,n,h,n,h,n,n,h,h,n,n,h,h,n,h,47.5,252"),
    c("49,Y,missionplanning,g,5,1980,semidetached,vh,n,xh,h,h,l,l,n,h,n,n,n,l,h,n,21,107"),
    c("50,Y,simulation,g,5,1983,semidetached,n,h,h,vh,n,n,h,h,h,h,n,h,l,l,h,78,571.4"),
    c("51,Y,simulation,g,5,1984,semidetached,n,h,h,vh,n,n,h,h,h,h,n,h,l,l,h,11.4,98.8"),
    c("52,Y,simulation,g,5,1985,semidetached,n,h,h,vh,n,n,h,h,h,h,n,h,l,l,h,19.3,155"),
    c("53,Y,missionplanning,g,5,1979,semidetached,h,n,vh,h,h,l,h,h,n,n,h,h,l,vh,h,101,750"),
    c("54,Y,missionplanning,g,5,1979,semidetached,h,n,h,h,h,l,h,n,h,n,n,n,l,vh,n,219,2120"),
    c("55,Y,utility,g,5,1979,semidetached,h,n,h,h,h,l,h,n,h,n,n,n,l,vh,n,50,370"),
    c("56,spl,datacapture,g,2,1979,semidetached,vh,h,h,vh,vh,n,n,vh,vh,vh,n,h,h,h,l,227,1181"),
    c("57,spl,batchdataprocessing,g,2,1977,semidetached,n,h,vh,n,n,l,n,h,n,vh,l,n,h,n,l,70,278"),
    c("58,de,avionicsmonitoring,g,2,1979,semidetached,h,l,h,n,n,l,l,n,n,n,n,h,h,n,l,0.9,8.4"),
    c("59,slp,operatingsystem,g,6,1974,semidetached,vh,l,xh,xh,vh,l,l,h,vh,h,vl,h,vl,vl,h,980,4560"),
    c("60,slp,operatingsystem,g,6,1975,embedded,n,l,h,n,n,l,l,vh,n,vh,h,h,n,l,n,350,720"),
    c("61,Y,operatingsystem,g,5,1976,embedded,h,n,xh,h,h,l,l,h,n,n,h,h,h,h,n,70,458"),
    c("62,Y,utility,g,5,1979,embedded,h,n,xh,h,h,l,l,h,n,n,h,h,h,h,n,271,2460"),
    c("63,Y,avionicsmonitoring,g,5,1971,organic,n,n,n,n,n,l,l,h,h,h,n,h,n,l,n,90,162"),
    c("64,Y,avionicsmonitoring,g,5,1980,organic,n,n,n,n,n,l,l,h,h,h,n,h,n,l,n,40,150"),
    c("65,Y,avionicsmonitoring,g,5,1979,embedded,h,n,h,h,n,l,l,h,h,h,n,h,n,n,n,137,636"),
    c("66,Y,avionicsmonitoring,g,5,1977,embedded,h,n,h,h,n,h,l,h,h,h,n,h,n,vl,n,150,882"),
    c("67,Y,avionicsmonitoring,g,5,1976,embedded,vh,n,h,h,n,l,l,h,h,h,n,h,n,n,n,339,444"),
    c("68,Y,avionicsmonitoring,g,5,1983,organic,l,h,l,n,n,h,l,h,h,h,n,h,n,l,n,240,192"),
    c("69,Y,avionicsmonitoring,g,5,1978,semidetached,h,n,h,n,vh,l,n,h,h,h,h,h,l,l,l,144,576"),
    c("70,Y,avionicsmonitoring,g,5,1979,semidetached,n,l,n,n,vh,l,n,h,h,h,h,h,l,l,l,151,432"),
    c("71,Y,avionicsmonitoring,g,5,1979,semidetached,n,l,h,n,vh,l,n,h,h,h,h,h,l,l,l,34,72"),
    c("72,Y,avionicsmonitoring,g,5,1979,semidetached,n,n,h,n,vh,l,n,h,h,h,h,h,l,l,l,98,300"),
    c("73,Y,avionicsmonitoring,g,5,1979,semidetached,n,n,h,n,vh,l,n,h,h,h,h,h,l,l,l,85,300"),
    c("74,Y,avionicsmonitoring,g,5,1982,semidetached,n,l,n,n,vh,l,n,h,h,h,h,h,l,l,l,20,240"),
    c("75,Y,avionicsmonitoring,g,5,1978,semidetached,n,l,n,n,vh,l,n,h,h,h,h,h,l,l,l,111,600"),
    c("76,Y,avionicsmonitoring,g,5,1978,semidetached,h,vh,h,n,vh,l,n,h,h,h,h,h,l,l,l,162,756"),
    c("77,Y,avionicsmonitoring,g,5,1978,semidetached,h,h,vh,n,vh,l,n,h,h,h,h,h,l,l,l,352,1200"),
    c("78,Y,operatingsystem,g,5,1979,semidetached,h,n,vh,n,vh,l,n,h,h,h,h,h,l,l,l,165,97"),
    c("79,Y,missionplanning,g,5,1984,embedded,h,n,vh,h,h,l,vh,h,n,n,h,h,h,vh,h,60,409"),
    c("80,Y,missionplanning,g,5,1984,embedded,h,n,vh,h,h,l,vh,h,n,n,h,h,h,vh,h,100,703"),
    c("81,hst,Avionics,f,2,1980,embedded,h,vh,vh,xh,xh,h,h,n,n,n,l,l,n,n,h,32,1350"),
    c("82,hst,Avionics,f,2,1980,embedded,h,h,h,vh,xh,h,h,h,h,h,h,h,h,n,n,53,480"),
    c("84,spl,Avionics,f,3,1977,embedded,h,l,vh,vh,xh,l,n,vh,vh,vh,vl,vl,h,h,n,41,599"),
    c("89,spl,Avionics,f,3,1977,embedded,h,l,vh,vh,xh,l,n,vh,vh,vh,vl,vl,h,h,n,24,430"),
    c("91,Y,Avionics,f,5,1977,embedded,vh,h,vh,xh,xh,n,n,h,h,h,h,h,h,n,h,165,4178.2"),
    c("92,Y,science,f,5,1977,embedded,vh,h,vh,xh,xh,n,n,h,h,h,h,h,h,n,h,65,1772.5"),
    c("93,Y,Avionics,f,5,1977,embedded,vh,h,vh,xh,xh,n,l,h,h,h,h,h,h,n,h,70,1645.9"),
    c("94,Y,Avionics,f,5,1977,embedded,vh,h,xh,xh,xh,n,n,h,h,h,h,h,h,n,h,50,1924.5"),
    c("97,gal,Avionics,f,5,1982,embedded,vh,l,vh,vh,xh,l,l,h,l,n,vl,l,l,h,h,7.25,648"),
    c("98,Y,Avionics,f,5,1980,embedded,vh,h,vh,xh,xh,n,n,h,h,h,h,h,h,n,h,233,8211"),
    c("99,X,Avionics,f,2,1983,embedded,h,n,vh,vh,vh,h,h,n,n,n,l,l,n,n,h,16.3,480"),
    c("100,X,Avionics,f,2,1983,embedded,h,n,vh,vh,vh,h,h,n,n,n,l,l,n,n,h,6.2,12"),
    c("101,X,science,f,2,1983,embedded,h,n,vh,vh,vh,h,h,n,n,n,l,l,n,n,h,3,38")])
  return t

def c(s):
    clean = re.sub(table.DIRT, "",s)
    cells = clean.split(table.SEP)
    return [ cell.strip() for cell in cells ]

class table:
  BINS = 5
  SEP  = ","
  DIRT = '([\n\r\t]|#.*)'
  def __init__(i,names= [],
                 types= [],
                 rows=  [],
                 decs = lambda x:  x[:-1][ :],
                 objs = lambda x: [x[ -1]][:]):
    i.names    = names
    i.types    = types
    i.decs     = decs
    i.objs     = objs
    i.rows     = []
  def data(i, rows):
    i.rows     = [ [ t(cell) for t, cell in zip(i.types, row) ]
                   for row in rows ]
    i.lo, i.hi = i.ranges()
    i.bins     = [ i.bins1(row) for row in i.rows ]
  def ranges(i):
    nums    = [ n for n,t in enumerate(i.types) if t == F or t == I ]
    print(nums)
    lo      = { n: 1e32 for n in nums }
    hi      = { n:-1e32 for n in nums }
    for row in i.rows:
      for n in lo:
        lo[n] = min(lo[n], row[n])
        hi[n] = max(lo[n], row[n])
    print(dict(lo=lo,hi=hi))
    return lo,hi
  def bins1(i,row):
    out = row[:]
    for n in i.lo:
      x,y,z  = out[n], i.lo[n], i.hi[n]
      b      = int((x - y) / (z - y + 1e-31) * table.BINS)
      b1     = b if b < table.BINS else table.BINS - 1
      out[n] = b1
      if n==22: print(n,x,y,z,b1)
    return i.decs(out) + i.objs(row)

t = nasa93()
#for x in t.bins: print(x)
