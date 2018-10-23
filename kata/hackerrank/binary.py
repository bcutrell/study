def to_bin(n):
  powers_of_two = [2**exp for exp in range(100) if 2**exp<n]
  result = []

  while len(powers_of_two) > 0:
    highest_power = powers_of_two.pop()

    if highest_power <= n:
      n -= highest_power
      result.append(1)
    else:
      result.append(0)

  return int(''.join([str(x) for x in result]))


def from_bin(n):
  bin_str = str(n)
  max_power = len(bin_str)-1
  result = 0

  for c in bin_str:
    num = int(c)
    
    if num == 1:
      result += 2**max_power
    max_power -= 1

  return result



assert(to_bin(20) == 10100)
assert(to_bin(27) == 11011)
assert(to_bin(114) == 1110010)

assert(from_bin(10100) == 20)
assert(from_bin(11011) == 27)
assert(from_bin(1110010) == 114)


