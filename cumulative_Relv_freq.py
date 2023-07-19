"""
calculating cumulative relative frequency / Pareto Distribution
In Statistics, a cumulative frequency is defined as the total 
of frequencies, that are distributed over different class intervals. 
"""
from reltv_frequency import reltiv_freq


def reltv_cum_freq(lst):
    reltv_freq = reltiv_freq(lst)
    temp_list = []
    temp = 0
    position = 1
    temp_list.append(reltv_freq[0])

    for i in reltv_freq:
        if position >= len(reltv_freq):
            break
        temp = reltv_freq[position] + temp_list[position-1]
        temp = round(temp, 2)
        temp_list.append(temp)
        position += 1
    return temp_list


lst = [119, 17, 11, 11, 11, 6, 4, 1, 1, 86]


test = reltv_cum_freq(lst)

for i in test:
    print(i)