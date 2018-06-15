'''
You have a function rand5() that generates a random integer from 1 to 5. Use it to write a function rand7() that generates a random integer from 1 to 7.

rand5() returns each integer with equal probability. rand7() must also return each integer with equal probability.
'''

import random

def rand5():
  return random.randint(1,5)

def rand7():
  while True:
    # Do our die rolls
    roll1 = rand5()
    roll2 = rand5()
    outcome_number = (roll1-1) * 5 + (roll2-1) + 1

    # If we hit an extraneous
    # outcome we just re-roll
    if outcome_number > 21:
      continue

  # Our outcome was fine. return it!
    return outcome_number % 7 + 1

for x in range(3):
  print(rand7())



