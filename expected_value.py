"""
Expected (E) value is the outcome weighted by its propbability (P)
"""

def expected_value(dic, repts):
    probLst = []
    outcome = []
    for o in dic.keys():
        outcome.append(o)

    for p in dic.values():
        probLst.append(p)

    counter = 0
    temp = 0
    expectedLst = []
    for i in range(len(probLst)):
        temp = outcome[counter] * probLst[counter]
        expectedLst.append(temp)
        counter += 1

    return sum(expectedLst) * repts
    

# workout = {0: 0.1,
#            1: 0.15,
#            2: 0.4,
#            3: 0.25,
#            4: 0.1}
# workout_exp = expected_value(workout, 12)

# print(workout_exp)

game = {1: 0.16,
        0: 0.83}

game_expct = expected_value(game, 1)

print(game_expct)


