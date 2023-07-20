"""
Calculating Median for the data
"""
import math


def median(lst):
    lst.sort()
    print(len(lst)+1)
    position = (len(lst)+1)/2
    # position += 1

    #
    print(position)

    up = 0
    low = 0
    if position%2 !=0:
        up = math.ceil(position)
        up = int(up)
        low = math.floor(position)
        low = int(low)
        print(up)
        print(low)
        print(f"The Median value at position {position}, between value: {lst[up-1]} & value: {lst[low-1]}")
        
    else:
        position = int(position)
        med = lst[position]
        print(f"The Median value {med-1}")


    return None


lst = [1,2,3,3,5,6,7,8,9,11,66]
lst2 = [1,2,3,4,5,6,7,8,9,10]

median(lst)
