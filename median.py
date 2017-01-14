"""
Return the median of a list of numbers. Cache this
calculation to avoid repeating a needless call to `sort`.
Note that `__add__` zaps that cache if ever a new number is added.
"""

def median(lst,ordered=False):
  assert lst,"median needs a non-empty list"
  n  = len(lst)
  p  = q  = n//2
  if n < 3:
    p,q = 0, n-1
  else:
    lst = lst if ordered else sorted(lst)
    if not n % 2:
      q = p -1
  return lst[p] if p==q else (lst[p]+lst[q])/2

