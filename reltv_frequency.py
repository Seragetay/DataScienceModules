"""
calculating Relative Frequency
A relative frequency indicates how often a specific kind of event 
occurs within the total number of observations.
"""

def reltiv_freq(lst):
    prcr_list = []
    temp = 0
    total = sum(lst)
    for i in lst:
        temp = (i/total) *100
        temp = round(temp,2)
        prcr_list.append(temp)
    return prcr_list


lst = [119, 17, 11, 11, 11, 6, 4, 1, 1, 86]

test = reltiv_freq(lst)

for i in test:
    print(i)