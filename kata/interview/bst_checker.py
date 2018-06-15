'''
Write a function to check that a binary tree ↴ is a valid binary search tree.

A binary search tree is a binary tree in which, for each node:

The node's value is greater than all values in the left subtree.
The node's value is less than all values in the right subtree.
BSTs are useful for quick lookups. If the tree is balanced, we can search for a given value in the tree in O(\lg{n})O(lgn) time.
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

# Depth first
def bst_checker(bst):
    if bst == None:
        return True
    
    nodes = [(bst, -float('inf'), float('inf'))]

    while len(nodes) > 0:
        node, lower_bound, upper_bound = nodes.pop()
        print(node.value, lower_bound, upper_bound)

        if (node.value <= lower_bound) or (node.value >= upper_bound):
            return False

        if node.left:
            nodes.append((node.left, lower_bound, node.value))
            
        if node.right:
            nodes.append((node.right, node.value, upper_bound))

    return True

t = BinaryTreeNode(9)
l=t.insert_left(8)
r=t.insert_right(10)
r=r.insert_left(8)

print(bst_checker(t))
