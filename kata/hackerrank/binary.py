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

  return ''.join([str(x) for x in result])


def from_bin(n):
  pass


assert(to_bin(20) == '10100')
assert(to_bin(27) == '11011')
assert(to_bin(114) == '1110010')

exit()
assert(from_bin(10100) == 20)
assert(from_bin(11011) == 27)
assert(from_bin(1110010) == 114)


