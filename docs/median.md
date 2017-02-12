Return the median of a list of numbers.
By default, assumes the list  is unordered
and needs sorting (and this default can be over-loaded
at the command line).

Whether or not to sort by default _sounds_ like a big
issue. However,  after several timing studies, I can report
that unless lists are large (10,000 items or more),
in absolute terms, it makes
very little difference to the runtimes (since
Python's built in sort functions can sort thousands
of numbers in ten-thousands of a second).

______
## Programmer's Guide

```python

# If `ordered` is `False`, do not sort `lst`
def median(lst,ordered=False):
  assert lst,"median needs a non-empty list"
  n  = len(lst)
  p  = q  = n//2
  if n < 3:
    p,q = 0, n-1
  else:
    lst = lst if ordered else sorted(lst)
    if not n % 2: # for even-length lists, use mean of mid 2 nums
      q = p -1
  return lst[p] if p==q else (lst[p]+lst[q])/2

```

