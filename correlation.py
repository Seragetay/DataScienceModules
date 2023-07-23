"""
In statistics, correlation or dependence is any statistical relationship, 
whether causal or not, between two random variables or bivariate data.
"""


from standard_deviation import standard_dev_smpl
from covariance import covariance_s

def correlation_s(lst1, lst2):
    cov = covariance_s(lst1, lst2)
    x_strd = standard_dev_smpl(lst1)
    y_strd = standard_dev_smpl(lst2)

    corl = cov/(x_strd * y_strd)

    return round(corl,2)

#Example 

writing = [344, 383, 611, 713, 536]
reading = [378, 349, 503, 719, 503]

corl = correlation_s(writing, reading)
print(corl)