"""
Covariance is a measure of the joint variability of two random variables. 
If the greater values of one variable mainly correspond with the greater 
values of the other variable, and the same holds for the lesser values, 
the covariance is positive.
"""

from mean import mean

def covariance_s(lst1, lst2):
    x_bar = round(mean(lst1))
    y_bar = round(mean(lst2))

    x_value = []
    temp = 0
    for x in lst1:
        temp = x - x_bar
        temp = round(temp, 2)
        x_value.append(temp)

    y_value = []
    temp = 0
    for y in lst2:
        temp = y - y_bar
        temp = round(temp,2)
        y_value.append(temp)

    counter = 0
    temp = 0
    values = []
    for v in range (len(y_value)):
        temp = x_value[counter] * y_value[counter]
        values.append(temp)
        counter += 1

        denom = len(x_value)
    print(sum(values))
    covar = sum(values)/(denom-1)

    return covar





