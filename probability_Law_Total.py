"""
P(A|B) = A/B
"""
"""Example below is assuming A is being a Vegi, so we need to find the probablity of being a vegi"""

v_male = 29 # Veg men
v_woman = 15 # Veg women
m_male = 24 # meat Men
m_woman = 32 # meat Women

totalSample = v_male + v_woman + m_male + m_woman
"""Law of Total Probability"""
"""P(A) = P(A|B1) * B1 + P(A|B2) * P(B2)"""
"""A = being vegan, B1 Male vegan, B2 Woman Vegan"""

vegit = (v_male/(v_male+m_male) * (v_male+m_male)/totalSample) + (v_woman/(v_woman+m_woman) * (v_woman+m_woman)/totalSample)


print(vegit)







