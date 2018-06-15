
def is_palindrome(word):
  counts = {}
  for c in word:
    if c in counts:
      counts[c] += 1
    else: 
      counts[c] = 1

  odds = 0
  for count in counts.values():
    if odds > 1:
      return False

    if count % 2 != 0:
      odds += 1 

  return True

print(is_palindrome('CATCOAT'))

# ('afiry', 8427)
# 26 * [0]

import code

def is_anagram(letters, words):
  letters = letters.replace(" ", "")

  # don't need this...
  sorted_words = [ (''.join(sorted(word)), idx) for idx, word in enumerate(words) ]
  sorted_letters = ''.join(sorted(letters))

  potentials = []
  for word in sorted_words:
    copy = sorted_letters[:]
    all_in = True
    for c in word[0]:
      if c in copy:
        copy = copy.replace(c, "")
      else:
        all_in = False

    if all_in == True:
      potentials.append(word)

  words = [words[t[1]] for t in potentials]

  # sort big list of words
  words.sort(key = lambda s: len(s), reverse=True)

  code.interact(local=locals())

  anagram = ""
  # while len(letters) > 0:

# "rail safety" = "fairy tales"
# "restful" = "fluster"
# "funeral" = "real fun"
# "adultery" = "true lady"
# "customers" = "store scum"
# "forty five" = "over fifty"

f = open('words.txt', 'r').read().split("\n")
is_anagram("rail safety", f)

