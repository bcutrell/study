class Node:
  def __init__(self,data):
    self.right=self.left=None
    self.data = data

class Solution:
  def insert(self,root,data):
    if root==None:
        return Node(data)
    else:
        if data<=root.data:
            cur=self.insert(root.left,data)
            root.left=cur
        else:
            cur=self.insert(root.right,data)
            root.right=cur
    return root

  def getHeight(self, root):
    """
    params: root

    find number of edges between the tree's root and its furthest leaf

    Using a depth-first search
    """

    depths = []
    nodes = []
    nodes.append((root, 0))

    while len(nodes):
      print(nodes)
      node, depth = nodes.pop()

      right = node.right
      left = node.left

      # We found a leaf
      if right == None and left == None:

        if depth not in depths:
          depths.append(depth)

      else:
        if node.left:
          nodes.append((node.left, depth + 1))
        if node.right:
          nodes.append((node.right, depth + 1))

    return max(depths)


# input
tree = [9,20,50,35,44,9,15,62,11,13]
correct_height = 4

length = tree.pop(0)
myTree=Solution()
root=None
for i in range(length):
  root=myTree.insert(root, tree[i])

height=myTree.getHeight(root)
assert height == correct_height
