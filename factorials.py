""" Factorials is the product of the natual numbers from 1 to n
    Example: n! = 1*2*3*4...n
    3! = 1*2*3 = 6
    Negative numbers do not have factorial.
    0! = 1
    ---------------------------------------------------------------
    Properties:
    n! = (n-1)! * n
    (n+1)! = n! * (n+1)

    Two Factorials: n > k
    n!/k! = (k+1) * (k+2) * (k+3)...n
"""


def fact(n):
    total = 0
    temp = 1
    if n == 0:
        n =1
    for i in range(1, n):
        temp = temp * (i + 1)
        total = temp
    
    if total == 0:
        total = 1
    return total


print(fact(1))
