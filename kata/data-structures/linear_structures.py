# Stacks - LIFO
# order collection of items were the additioin of new items and the removal of 
# existing items always takes place at the same end

# Queue - FIFO
# order collection of items were the additioin of new items happens at one end, called the "rear", 
# and the removal of  existing items occurs at the other end, commonly called the front

# Deque - FIFO or LIFO
# A double ended queue, items can be added/removed to the front or rear


'''
Given a string of opening and closing parentheses, check whether it’s balanced. 
We have 3 types of parentheses: round brackets: (), square brackets: [], 
and curly brackets: {}. 
Assume that the string doesn’t contain any other character than these, 
no spaces words or numbers. As a reminder, 
balanced parentheses require every opening parenthesis to be closed 
in the reverse order opened. For example ‘([])’ is balanced but ‘([)]’ is not.

You can assume the input string has no spaces.
'''

CHARS = {
"(": ")",
"[": "]",
"{": "}"
}

def balance_check(s):
  os = []

  for char in s:
    if char in CHARS.keys():
      os.append(char)
    elif char in CHARS.values():
      if char != CHARS[os.pop()]:
        return False
    else:
      return "Invalid char"

  if len(os) == 0:
    return True
  else:
    return False

"""
RUN THIS CELL TO TEST YOUR SOLUTION
"""
from nose.tools import assert_equal

class TestBalanceCheck(object):
      
  def test(self,sol):
    assert_equal(sol('[](){([[[]]])}('),False)
    assert_equal(sol('[{{{(())}}}]((()))'),True)
    assert_equal(sol('[[[]])]'),False)
    print('ALL TEST CASES PASSED')
                        
# Run Tests
t = TestBalanceCheck()
t.test(balance_check)


'''
Given the Stack class below, implement a Queue class using two stacks! 
Note, this is a "classic" interview problem. Use a Python list data structure as your Stack.
'''

# Uses lists instead of your own Stack class.
stack1 = []
stack2 = []

class Queue2Stacks(object):
      
  def __init__(self):
    # Two Stacks
    self.stack1 = []
    self.stack2 = []

  def enqueue(self,element):
    self.stack1.append(element)

  def dequeue(self):
    if len(self.stack2) > 0:
      return self.stack2.pop()
    else:
      if len(self.stack1) == 0:
        return None
      else:
        while len(self.stack1) > 0:
          self.stack2.append(self.stack1.pop())
        return self.stack2.pop()

"""
RUN THIS CELL TO CHECK THAT YOUR SOLUTION OUTPUT MAKES SENSE AND BEHAVES AS A QUEUE
"""
q = Queue2Stacks()
for i in range(5):
  q.enqueue(i)

for i in range(5):
  print(q.dequeue())

