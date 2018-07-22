'''
Given a singly linked list, write a function which takes in the first node in a singly linked list and returns a boolean indicating if the linked list contains a "cycle".

A cycle is when a node's next point actually points back to a previous node in the list. This is also sometimes known as a circularly linked list.

You've been given the Linked List Node class code:
'''

class Node(object):
      
  def __init__(self,value):
    self.value = value
    self.nextnode = None


def cycle_check(node):
  car1 = node
  car2 = node
  while car1 != None and car2.nextnode != None:
    car1 = car1.nextnode
    car2 = car2.nextnode.nextnode
    if car1 == car2:
      return True

  return False



"""
RUN THIS CELL TO TEST YOUR SOLUTION
"""
from nose.tools import assert_equal

# CREATE CYCLE LIST
a = Node(1)
b = Node(2)
c = Node(3)

a.nextnode = b
b.nextnode = c
c.nextnode = a # Cycle Here!


# CREATE NON CYCLE LIST
x = Node(1)
y = Node(2)
z = Node(3)

x.nextnode = y
y.nextnode = z

#############
class TestCycleCheck(object):
      
  def test(self,sol):
    assert_equal(sol(a),True)
    assert_equal(sol(x),False)
    print("ALL TEST CASES PASSED")

# Run Tests

t = TestCycleCheck()
t.test(cycle_check)


'''
Write a function to reverse a Linked List in place. The function will take in the head of the list as input and return the new head of the list.

You are given the example Linked List Node class:
'''
def reverse(head):
  current = head
  previous = None
  nextnode = None

  while current:
    nextnode = current.nextnode
    current.nextnode = previous
    previous = current
    current = nextnode

  return previous

# Create a list of 4 nodes
a = Node(1)
b = Node(2)
c = Node(3)
d = Node(4)

# Set up order a,b,c,d with values 1,2,3,4
a.nextnode = b
b.nextnode = c
c.nextnode = d
try:
  d.nextnode.value # should fail
except:
  print('Ready to reverse')

print(a.nextnode.value)
print(b.nextnode.value)
print(c.nextnode.value)
reverse(a)
print(d.nextnode.value)
print(c.nextnode.value)
print(b.nextnode.value)

try:
  print(a.nextnode.value)
except:
  print('PASS')


'''
Write a function that takes a head node and an integer value n and then returns the nth to last node in the linked list. For example, given:
'''


def nth_to_last_node(n, head):
  node_values = []
  node = head.nextnode

  while node:
    node_values.append(node)
    node = node.nextnode
  return node_values[-n]


"""
RUN THIS CELL TO TEST YOUR SOLUTION AGAINST A TEST CASE 

PLEASE NOTE THIS IS JUST ONE CASE
"""

from nose.tools import assert_equal

a = Node(1)
b = Node(2)
c = Node(3)
d = Node(4)
e = Node(5)

a.nextnode = b
b.nextnode = c
c.nextnode = d
d.nextnode = e

####

class TestNLast(object):
      
  def test(self,sol):
    assert_equal(sol(2,a),d)
    print('ALL TEST CASES PASSED')

# Run tests
t = TestNLast()
t.test(nth_to_last_node)


