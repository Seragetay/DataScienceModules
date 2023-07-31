"""
In probability theory and statistics, the binomial distribution 
with parameters n and p is the discrete probability distribution 
of the number of successes in a sequence of n independent experiments, 
each asking a yes–no question, and each with its own Boolean-valued 
outcome: success or failure.

P(desired outcome) = p
p(alternative outcome) = p-1

p(y) = (Combintorix of p many times out of n) * p to the power of y 
* (1-p) to the power n -y
n = many trials
y = number of times we wish to happen
p = preferred outcome
"""

from combinations import combinations
from power import power
import math

def b(n, y, p):
    prop_funct = combinations(n, y)* power(p,y) * power((1-p), (n-y))
    expected_value = p * n
    variance = n * p  * (1-p)
    strd_dev = math.sqrt(variance)

    print(f"Probability function = {round(prop_funct, 4)} \nExpected Value = {round(expected_value, 2)}\nVariance = {round(variance,2)} \nStandard Deviation = {round(strd_dev, 2)}")

test = b(5,3, 0.6)

print(test)


