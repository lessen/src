pypy=$(HOME)/opt/pypy/bin/pypy3

eg0:
	time -p $(pypy) bore2.py

eg1:
	@ python3 bore2.py                  \
	| sed -e "s/[,\'\[]//g" -e 's/\]//'\
	| sort -t, -n                       \
	| column  -t                         
	
eg2:
	@ python3 bore2.py                  \
	| sed -e "s/[,\'\[]//g" -e 's/\]//'\
	| sort -t, -n                       \
	| column  -t                         \
	| gawk '{print $$23}'                  \
	| sort -n                              \
	| uniq -c
