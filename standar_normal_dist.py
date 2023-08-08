from mean import mean
from standard_deviation import standard_dev_smpl
import pandas as pd

def normilzing_n_dist(lst: list):
    strd_list = []
    tem_val = 0
    x̄ = mean(lst)
    s = standard_dev_smpl(lst)

    for i in lst:
        tem_val = i - x̄
        tem_val = tem_val/s

        strd_list.append(tem_val)
    x̄_s = round(mean(strd_list))
    s_s = round(standard_dev_smpl(strd_list))

    stardard_mean = x̄_s
    standard_strd = s_s

    print(f"Standardized Mean = {stardard_mean}")
    print(f"Standardized Standard Deviation = {standard_strd}")

    return strd_list

data = pd.read_excel("C:/Users/Serage/Documents/Learning/Data Science Class/test files/3.4.Standard-normal-distribution-exercise.xlsx", sheet_name='Sheet1')

test_list = []

for item in data.Original_dataset:
    test_list.append(item)
#print(test_list)
testing = normilzing_n_dist(test_list)
# for n in testing:
#     print(n)



        

            

