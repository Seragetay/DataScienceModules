"""
Calculating the Mean
"""
def mean(lst):
    mu = 0
    temp = 0
    for i in lst:
        temp += i
    mu = temp/len(lst)
    mu = round(mu, 2)
    #print(f'The total number is {temp}. the N value is {len(lst)}')
    #print(f"Mean = {mu}")
    return mu


    
