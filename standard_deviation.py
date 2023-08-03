import math
from veriance import var_pop, var_sample


def standard_dev_smpl(lst):
    strd_div = var_sample(lst)
    strd_div = math.sqrt(strd_div)
    return strd_div

def standard_dev_pop(lst):
    strd_div = var_pop(lst)
    strd_div = math.sqrt(strd_div)
    return strd_div

