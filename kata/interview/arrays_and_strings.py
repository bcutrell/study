
'''
Implement a method to perform basic string compression using the counts of repeated characters. 
For example, aabbcccccaaa would become a2b1c5a3. 
If the 'compressed' string is not smaller than the original, return the original.
'''
def compress_str(word):
  count = 1
  compressed_str = ""
  last = None

  for c in word:

    # ignore the first char and set last
    if last == None:
      last = c
      continue

    if c == last:
      count += 1
    else:
      compressed_str += (last + str(count))
      count = 1

    last = c

  # add the last piece after the loop
  compressed_str += (last + str(count))

  if len(compressed_str) < len(word):
    return compressed_str
  else:
    return word

result = compress_str('aabcccccaaa')
print(result)

'''
Given an image represented by an NxN matrix, where each pixel in the image is 4 bytes
write a method to totate the image by 90 degrees
'''

def rotate(matrix):
  rotated_matrix = []
  size = len(matrix)

  for n in matrix:
    rotated_matrix.append([])

  for row_idx, row in enumerate(matrix):
    for col_idx, col in enumerate(row):
      rotated_matrix[col_idx].insert(0, col)

  return rotated_matrix

result = rotate([ [0,1,0], [1,0,1], [0,0,1] ])
print(result)

