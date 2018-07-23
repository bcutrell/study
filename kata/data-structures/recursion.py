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

