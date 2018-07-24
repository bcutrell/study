'''
Problem 1

Write a recursive function which takes an integer and computes the cumulative sum of 0 to that integer
For example, if n=4 , return 4+3+2+1+0, which is 10.
'''

def rec_sum(n):

  # Base case
  if n == 0:
    return 0

  return n + rec_sum(n-1)

assert rec_sum(4) == 10
print('Problem 1 - PASS')


'''
Problem 2

Given an integer, create a function which returns the sum of all the individual digits in that integer. For example: if n = 4321, return 4+3+2+1
'''

def sum_func(n):

  # Base case
  if n == 0:
    return 0
  return n % 10 + sum_func(n // 10)

assert sum_func(4321) == 10
print('Problem 2 - PASS')

'''
Problem 3

Create a function called word_split() which takes in a string phrase and a set list_of_words. 
The function will then determine if it is possible to split the string in a way 
in which words can be made from the list of words. 
You can assume the phrase will only contain words found in the dictionary if it is completely splittable.

'''

def word_split(phrase,list_of_words, output = None):
  if output == None:
    output = []

  for word in list_of_words:

    if phrase.startswith(word):
      output.append(word)

      return word_split(phrase[len(word):],list_of_words, output)

  return output
  

assert word_split('themanran',['the','ran','man']) == ['the', 'man', 'ran']
assert word_split('ilovedogsJohn',['i','am','a','dogs','lover','love','John']) ==  ['i', 'love', 'dogs', 'John']
assert word_split('themanran',['clown','ran','man']) == []
print('Problem 3 - PASS')


def reverse(s):
  if len(s) == 1:
    return s

  return s[-1] + reverse(s[:-1])

'''
TEST
'''

from nose.tools import assert_equal

class TestReverse(object):
      
  def test_rev(self,solution):
    assert_equal(solution('hello'),'olleh')
    assert_equal(solution('hello world'),'dlrow olleh')
    assert_equal(solution('123456789'),'987654321')
    print('Reverse Problem - PASS')

# Run Tests
test = TestReverse()
test.test_rev(reverse)

def permute(s):
  '''
  permute('abc')
  > ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
  '''
  out = []

  # Base case
  if len(s) == 1:
    out = [s]

  else:
    for i, let in enumerate(s):

      for perm in permute( s[:i] + s[i+1:] ):
        out += [let + perm]

  return out


  idx = 0
  for char in s:
    oc = s[:idx] + s[idx+1:] # grab all other chars
    result = char + permute(oc)
    perms.append(result)
    print(perms)
    idx += 1

  return perms


def permute_iter(s):
  # 1. iterate through string
  idx = 0
  for char in s:
    oc = s[:idx] + s[idx+1:] # grab all other chars

    # 2. get the permutation of all remaing strings
    # 3. add perms to initial string
    perms.append(char + oc[0] + oc[1])
    perms.append(char + oc[1] + oc[0])
    idx += 1

  return perms

"""
TEST
"""

class TestPerm(object):
  def test(self,solution):
    assert_equal(sorted(solution('abc')),sorted(['abc', 'acb', 'bac', 'bca', 'cab', 'cba']))
    assert_equal(sorted(solution('dog')),sorted(['dog', 'dgo', 'odg', 'ogd', 'gdo', 'god']) )
    print('Permutation Problem - PASS')

# Run Tests
t = TestPerm()
t.test(permute)

def fib_rec(n):
  '''
  fib_rec(10)
  > 55
  '''

  # Base case
  if n == 0 or n ==1:
    return n
  else:
    return fib_rec(n-1) + fib_rec(n-2)



# Instantiate Cache information
def fib_dyn(n):
  cache = [None] * (n + 1)

  if n == 0 or n == 1:
    return n

  elif cache[n] != None:
    return cache[n]

  else:
    fib_n = fib_rec(n-1) + fib_rec(n-2) 
    cache[n] = fib_n
    return cache[n]

def fib_iter(n):
  fibs = [0,1,1]
  if n > 2:
    for x in range(n-2):
      fibs.append(fibs[-1] + fibs[-2])

  return fibs[n]

"""
TEST
"""

from nose.tools import assert_equal

class TestFib(object):
      
  def test(self,solution):
    assert_equal(solution(10),55)
    assert_equal(solution(1),1)
    assert_equal(solution(23),28657)
    print('Fibonacci Problem - PASS')

# UNCOMMENT FOR CORRESPONDING FUNCTION
t = TestFib()
t.test(fib_rec)
t.test(fib_dyn) # Note, will need to reset cache size for each test!
t.test(fib_iter)

'''
Given a target amount n and a list (array) of distinct coin values, what's the fewest coins needed to make the change amount.

For example:

If n = 10 and coins = [1,5,10]. Then there are 4 possible ways to make change:

1+1+1+1+1+1+1+1+1+1

5 + 1+1+1+1+1

5+5

10

With 1 coin being the minimum amount.
'''

def rec_coin(target,coins):
  pass


rec_coin(10,[1,5])

class TestCoins(object):
      
  def check(self,solution):
    coins = [1,5,10,25]
    assert_equal(solution(45,coins),3)
    assert_equal(solution(23,coins),5)
    assert_equal(solution(74,coins),8)
    print('Coin Problem - PASS')

# Run Test
test = TestCoins()
test.check(rec_coin)

