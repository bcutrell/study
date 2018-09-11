'''
Emma is playing a new mobile game that starts with consecutively numbered clouds. Some of the clouds are thunderheads and others are cumulus. She can jump on any cumulus cloud having a number that is equal to the number of the current cloud plus  or . She must avoid the thunderheads. Determine the minimum number of jumps it will take Emma to jump from her starting postion to the last cloud. It is always possible to win the game.

For each game, Emma will get an array of clouds numbered  if they are safe or  if they must be avoided. For example,  indexed from . The number on each cloud is its index in the list so she must avoid the clouds at indexes  and . She could follow the following two paths:  or . The first path takes  jumps while the second takes .
'''

def jumpingOnClouds(arr):
  jumps = 0
  i = 0

  while i+2 <= len(arr):
    if i+2 >= len(arr):
      jumps += 1
      break

    next_next_cloud = arr[i+2]

    if next_next_cloud == 0:
      jumps += 1
      i += 2
    else:
      jumps += 1
      i += 1
  return jumps


test = [0,0,1,0,0,1,0]
assert(jumpingOnClouds(test) == 4)

test = [0,0,0,0,0,1,0]
assert(jumpingOnClouds(test) == 3)

test = [0,0,0,1,0,0]
assert(jumpingOnClouds(test) == 3)
