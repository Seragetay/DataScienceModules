from power import power
from factorials import fact

"""
Variations with repetition
--n
Vp = n to the power of p

p = the spots available
n = the options available

"""


def varWrepit(n, p):
    v = power(n, p)
    return v

test = varWrepit(26, 4)
print(test)

"""
Variation with no repitition
When we use on option in a spot we can not use it again for the remaining spots.
  n
 V = n!/(n-p)!
  p
"""

def varNoRepit(n, p):
    v = fact(n)/fact(n-p)
    return v
test2 = varNoRepit(5, 4)
print(test2)