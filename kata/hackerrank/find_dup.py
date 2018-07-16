'''
Find a duplicate, Space Edition™.

We have a list of integers, where:

The integers are in the range 1..n
The list has a length of n+1
It follows that our list has at least one integer which appears at least twice. But it may have several duplicates, and each duplicate may appear more than twice.

Write a function which finds an integer that appears more than once in our list. (If there are multiple duplicates, you only need to find one of them.)

We're going to run this function on our new, super-hip MacBook Pro With Retina Display™. Thing is, the damn thing came with the RAM soldered right to the motherboard, so we can't upgrade our RAM. So we need to optimize for space!
'''

def find_repeat(numbers):
  '''
  1. Do an in-place sort of the list (for example an in-place merge sort).
  2. Walk through the now-sorted list from left to right.
  3. Return as soon as we find two adjacent numbers which are the same.
  '''



