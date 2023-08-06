"""Additive Law"""
"""P(A|B) = P(A)+P(B)-P(Intersect A and B)"""

"""Example below need to find the probability of being a woman and vegis"""
"""P(Woman and veg) = P(woman) + P(vegan) - (woman and vegan)"""

v_male = 29 # Veg men
v_woman = 15 # Veg women
m_male = 24 # meat Men
m_woman = 32 # meat Women

totalSample = v_male + v_woman + m_male + m_woman

Pvg_woman = (((v_woman + m_woman)/totalSample) + ((v_woman+v_male)/totalSample)) - (v_woman/totalSample)

print(Pvg_woman)

"""Example Blow a probablity of being a man and vegan"""

Pm_v = ((v_male + m_male)/totalSample) + ((v_male+v_woman)/totalSample) - (v_male/totalSample) 
print(Pm_v)


"""Another example"""
"""Some one can implement SQL and Tableaue together"""
p_tableaue = 0.38
p_sql = 0.45
p_sql_tab = 0.66

sql_tab = (p_tableaue + p_sql) - p_sql_tab
print(sql_tab)
