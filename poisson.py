"""
In probability theory and statistics, the Poisson distribution is a discrete
 probability distribution that expresses the probability of a given number of 
 events occurring in a fixed interval of time or space if these events occur 
 with a known constant mean rate and independently of the time since the last 
 event.

 P(Y) = λ to the power of y by e / y factorial
"""
from power import power
from factorials import fact
import math


e = 2.72 # Constant number Euler's number

def po(y, λ):
    p = ((power(λ, y)) * (1/power(e, λ)))/ fact(y)
    expected_value = λ
    var = λ
    mean = λ
    str_dev = math.sqrt(λ)
    print(f"Propbablity = {round(p,2)}")
    print(f"Expected Value = {expected_value}")
    print(f"Variance = {var}")
    print(f"Mean = {mean}")
    print(f"Standard Deviation = {str_dev}")



po(7, 4)


