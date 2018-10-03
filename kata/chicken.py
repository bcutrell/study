'''
1) A farmer raises cows and chickens on his farm. His animals have a total of 24 heads and 68 legs. 
How many cows and how many chickens does he have?

- build a solver that will take any number of heads and legs and output the number of cows and chickens. 
 Should return an error if it is impossible to do with cows and chickens.

- bonus: allow for 1-legged chickens and/or 3-legged cows 
'''

import code; # code.interact(local=dict(globals(), **locals()))

def all_possible_combos(goal, unit_list):
    print(goal, unit_list)
    if goal == 0:
        return [[0] * len(unit_list)]

    if len(unit_list) == 0:
        return []

    unit = unit_list[0]
    remaining_unit_list = unit_list[1:]
    max_count = goal // unit

    results = []
    for i in range(max_count + 1):

      for s in all_possible_combos(goal - i * unit, remaining_unit_list):
        results.append([i] + s)
        print(unit, remaining_unit_list, max_count, i, s)

    return results


found = False

# 24 heads
# 68 legs
result = all_possible_combos(68, [2,4])
for x in result:
  if sum(x) == 24:
    chickens, cows = x
    found = True
    print('Chickens %s, Cows %s' % (chickens, cows))

if not found:
  print('No possible combination')
