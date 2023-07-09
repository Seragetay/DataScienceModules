"""
P(A|B) = P(B|A) * P(A)/P(B)

Example: experience = 45%, A+ students = 60%, P(A+|Exp) = 50
"""

def bays(ba, a, b):
    P_AB = ((ba) * a)/b
    return P_AB

test3 = bays(0.5, 0.45, 0.6)

print(test3)

test4 = bays(0.6, 0.4, 0.3)
print(test4)