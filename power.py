"""
Power function defined below
"""

def power(n,p):
    total = 0
    temp = n
    for i in range(1, p):
        temp = temp * n
        total = temp
    return total
    
test = power(26, 7)
print(test)

