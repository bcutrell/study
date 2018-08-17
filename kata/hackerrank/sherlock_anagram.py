def sherlockAndAnagrams(s):
  anag = 0
  map = {}
  for i in range(len(s)):
    for j in range(len(s) - i):
      s1 = ''.join(sorted(s[j:j + i + 1]))
      map[s1] = map.get(s1, 0) + 1
  for key in map:
    anag += (map[key] - 1) * map[key] // 2
  return anag

test = 'kkkk'
result = sherlockAndAnagrams(test)
expected = 10
print(result, expected)

test = 'abba'
result = sherlockAndAnagrams(test)
expected = 4
print(result, expected)

print(sherlockAndAnagrams('mom'))
test = 'ifailuhkqq'
result = sherlockAndAnagrams(test)
expected = 3
print(result, expected)

test = 'abcd'
result = sherlockAndAnagrams(test)
expected = 0
print(result, expected)



