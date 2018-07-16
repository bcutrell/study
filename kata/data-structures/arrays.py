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

  print(word1_count)
  print(word2_count)
  return word1_count == word2_count

"""
RUN THIS CELL TO TEST YOUR SOLUTION
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

