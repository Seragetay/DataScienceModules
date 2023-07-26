"""
It is a descreat distrbution.
1 Trial and 2 possible outcomes
Expected value = P (Favorable outcome)
Provide a dictionary assign key 1 to your favorit value, and zero to any 
other value.
Variance always = p(1-p)
"""



def bern(p):
    expectedValue = p[1]
    var = p[1]*(1-p[1])

    print(f"Expected value = {expectedValue} \nVariance = {var}")
    return expectedValue, var

values = {0: 0.4,
          1: 0.6}

test = bern(values)



