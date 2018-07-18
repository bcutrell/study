"""
anagram check
"""

def count_letters(word):
  count = {}
  for w in word:
    if w == " ":
      continue

    if w in count:
      count[w] += 1
    else:
      count[w] = 1
  return count

def anagram(word1, word2):
  word1_count = count_letters(word1)
  word2_count = count_letters(word2)

  return word1_count == word2_count

"""
TEST YOUR SOLUTION
"""
from nose.tools import assert_equal

class AnagramTest(object):
      
  def test(self,sol):
    assert_equal(sol('go go go','gggooo'),True)
    assert_equal(sol('abc','cba'),True)
    assert_equal(sol('hi man','hi     man'),True)
    assert_equal(sol('aabbcc','aabbc'),False)
    assert_equal(sol('123','1 2'),False)
    print("ALL TEST CASES PASSED")

t = AnagramTest()
t.test(anagram)

"""
pair sum
"""

def pair_sum(arr,k):
  idx = 0
  count = 0
  pairs = set() # avoid duplicate pairs

  for n1 in arr:
    inner_idx = 0

    for n2 in arr:
      if idx <= inner_idx:
        inner_idx += 1
        continue
      elif (n1 + n2) == k:
        pair = [n1,n2]
        pairs.add((min(pair), max(pair)))

      inner_idx += 1

    idx += 1

  return len(pairs)


"""
TEST YOUR SOLUTION
"""

class TestPair(object):
      
  def test(self,sol):
    assert_equal(sol([1,9,2,8,3,7,4,6,5,5,13,14,11,13,-1],10),6)
    assert_equal(sol([1,2,3,1],3),1)
    assert_equal(sol([1,3,2,2],4),2)
    print('ALL TEST CASES PASSED')

# Run tests
t = TestPair()
t.test(pair_sum)


'''
Find the Missing Element
Problem
Consider an array of non-negative integers. A second array is formed by shuffling the elements 
of the first array and deleting a random element. 
Given these two arrays, find which element is missing in the second array.

Here is an example input, the first array is shuffled and the number 5 is removed to construct the second array.

Input:

finder([1,2,3,4,5,6,7],[3,7,2,1,4,6])

Output:

5 is the missing number
'''

def finder(arr1,arr2):
  for n in arr2:
    arr1.remove(n)

  return arr1[0]
      

"""
TEST YOUR SOLUTION
"""

class TestFinder(object):
      
  def test(self,sol):
    assert_equal(sol([5,5,7,7],[5,7,7]),5)
    assert_equal(sol([1,2,3,4,5,6,7],[3,7,2,1,4,6]),5)
    assert_equal(sol([9,8,7,6,5,4,3,2,1],[9,8,7,5,4,3,2,1]),6)
    print('ALL TEST CASES PASSED')

# Run test
t = TestFinder()
t.test(finder)

'''
Given an array of integers (positive and negative) find the largest continuous sum.
'''

def large_cont_sum(arr): 
  if len(arr) <= 2:
    return max(arr)

  sums = set()


  idx = 1 # start at 1
  for x in arr:
    running_sums = x
    for y in arr[idx:]:
      running_sums +=  y
      sums.add(running_sums)

    idx += 1
  return max(sums)


class LargeContTest(object):
  def test(self,sol):
    assert_equal(sol([1,2,-1,3,4,-1]),9)
    assert_equal(sol([1,2,-1,3,4,10,10,-10,-1]),29)
    assert_equal(sol([-1,1]),1)
    print('ALL TEST CASES PASSED')

# Run Test
t = LargeContTest()
t.test(large_cont_sum)


'''
Given a string of words, reverse all the words
ignore all leading and trailling whitespace
'''

def rev_word(s):
  words = []
  for word in s.split(" "):
    if word != "":
      words.insert(0, word)

  return " ".join(words)


"""
TEST YOUR SOLUTION
"""

from nose.tools import assert_equal

class ReversalTest(object):
      
  def test(self,sol):
    assert_equal(sol('    space before'),'before space')
    assert_equal(sol('space after     '),'after space')
    assert_equal(sol('   Hello John    how are you   '),'you are how John Hello')
    assert_equal(sol('1'),'1')
    print("ALL TEST CASES PASSED")

# Run and test
t = ReversalTest()
t.test(rev_word)

'''
Given a string in the form 'AAAABBBBCCCCCDDEEEE' compress it to become 'A4B4C5D2E4'. 
For this problem, you can falsely "compress" strings of single or double letters. 
For instance, it is okay for 'AAB' to return 'A2B1' even though this technically takes more space.

The function should also be case sensitive, so that a string 'AAAaaa' returns 'A3a3'.
'''

def compress(s):
  idx=0
  cstring = ""
  c = 1

  for char in s:
    if len(s) > idx+1 and s[idx].lower() == s[idx+1].lower():
      c += 1
    else:
      cstring += char + str(c)
      c = 1
    idx += 1

  return cstring


"""
TEST YOUR SOLUTION
"""

class TestCompress(object):

  def test(self, sol):
    assert_equal(sol(''), '')
    assert_equal(sol('AABBCC'), 'A2B2C2')
    assert_equal(sol('AAABCCDDDDD'), 'A3B1C2D5')
    print('COMPRESS TEST CASES PASSED')

# Run Tests
t = TestCompress()
t.test(compress)


'''
Given a string,determine if it is compreised of all unique characters. 
For example, the string 'abcde' has all unique characters and should return True. The string 'aabcde' contains duplicate characters and should return false.
'''

def uni_char(s):
  chars = set()
  for c in s:
    if c in chars:
      return False
    else:
      chars.add(c)

  return True

"""
TEST YOUR CODE
"""

class TestUnique(object):

  def test(self, sol):
    assert_equal(sol(''), True)
    assert_equal(sol('goo'), False)
    assert_equal(sol('abcdefg'), True)
    print('UNIQUE TEST CASES PASSED')
                                                
# Run Tests
t = TestUnique()
t.test(uni_char)

