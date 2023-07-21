from variations import varNoRepit
from factorials import fact
"""
Combinations does not look to the order of the group, and it avoids double 
counting
 n
C = n!/P!(n-p)!
 p 
p = desired number of selection
n = available options
Symmetry is a property of a combination: example: picking 3 employees out of 10 is 
similar to choose 7 out of 10
n = 10
p = 7
"""
def combinations(n, p):
    c = varNoRepit(n, p)/fact(p)
    return c




