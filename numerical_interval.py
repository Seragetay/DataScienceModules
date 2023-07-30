"""
Numerical Interval
"""

def intervals(lst):
    mx = max(lst)
    print(mx)
    mn = min(lst)
    print(mn)

    min_max = mx - mn
    print(min_max)

    interval = int(input("Please enter interval: "))

    classwidth = round(min_max/interval)
    print(classwidth)

    lst.sort()
    
    # Buckets
    frequancy = 0
    for i in range(0, interval):
        start = mn
        end = start + classwidth
        for v in range(start, end):
            for k in lst:
                if k == v:
                    frequancy += 1
    
        print(f"{mn} to {(mn+5)-1} Frequency = {frequancy}")
        mn = mn+5
        frequancy = 0

    
    return classwidth
    


#Example 

lst = [96,98,97,96,83,95,78,88,79,95,85,98,99,93,73,79,78,83,90,96,90,91,91,89,99,99,88,94,95,96,96,66,82,90,91,73,87,97,73]

# for num in range(0, 100):
#     temp = random.randint(66, 98)
#     lst.append(temp)

itc = intervals(lst)

print(itc)
print(lst)














