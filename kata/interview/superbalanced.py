'''
A tree is "superbalanced" if the difference between the depths of any two leaf nodes
(A leaf node is a tree node with no children, 
It's the "end" of a path to the bottom, from the root)

is no greater than one.
Here's a sample binary tree node class:
'''

class BinaryTreeNode(object):

  def __init__(self, value):
    self.value = value
    self.left  = None
    self.right = None

  def insert_left(self, value):
    self.left = BinaryTreeNode(value)
    return self.left

  def insert_right(self, value):
    self.right = BinaryTreeNode(value)
    return self.right

# depth first walk
def is_superbalanced(btn):
  if btn == None:
    return True

  nodes = [(0, btn)]
  depths = []
  while len(nodes) > 0:
    depth, node = nodes.pop()

    if node.left == None and node.right == None:
      if depth not in depths:
        depths.append(depth)

      if (len(depths) > 2) or (len(depths) == 2 and abs(depths[0] - depths[1] > 1)):
        return False

    else:
      if node.left:
        nodes.append((depth+1, node.left))

      if node.right:
        nodes.append((depth+1, node.right))

  return True


t = BinaryTreeNode(10)
l=t.insert_left(12)
r=t.insert_right(8)

# l_l1=l.insert_left(14)
# l_r1=l.insert_right(10)

r_r1=r.insert_left(6)
r_l1=r.insert_right(8)

r1_r1=r_r1.insert_left(6)

r1_r2=r_r1.insert_right(3)
r1_r2=r1_r2.insert_right(2)

print(is_superbalanced(t))

