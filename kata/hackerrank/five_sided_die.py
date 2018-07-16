'''
You have a function rand7() that generates a random integer from 1 to 7. 
Use it to write a function rand5() that generates a random integer from 1 to 5.

rand7() returns each integer with equal probability. rand5() must also return each integer with equal probability.
'''
import random

def rand7():
  return random.randint(1,7)

def rand5():
  result = 7
  while result > 5:
    result = rand7()
  return result

for x in range(3):
  print(rand5())
