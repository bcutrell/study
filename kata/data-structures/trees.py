# node: name -> key, payload -> additional information
# edge: connects two nodes

# root: only node that has no incoming edges 
# path: ordered list of nodes that are connected by edges
# level: the level of a node "n" is the number of edges on the path from root node to n
# heght: max level at any point in the tree

# binary tree -> each node has a max of 2 children

# Tree Traversal
# 1. preorder
#    visit root first, then left, then right
# 2. inorder
#    visit left first, then root, then right
# 3. postorder
#    visit left first, then right, then root

# list of lists tree
def BinaryTree(r):
  return [r, [], []]

def insertLeft(root, newBranch):
  t = root.pop(1)

  if len(t) > 1:
    root.insert(1, [newBranch, t,[]])
  else:
    root.insert(1, [newBranch, [],[]])

  return root

def insertRight(root, newBranch):
  t = root.pop(2)

  if len(t) > 1:
    root.insert(2, [newBranch, [], t])
  else:
    root.insert(2, [newBranch, [],[]])

  return root

def getRootVal(root):
  return root[0]

def setRootVal(root, newVal):
  root[0] = newVal
  return root

def getLeftChild(root):
  return root[1]

def getRightChild(root):
  return root[2]

class BinaryTree(object):
  def __init__(self, rootObj):
    self.key = rootObj
    self.leftChild = None
    self.rightChild = None


  def insertLeft(self, newNode):
    # no left child
    if self.leftChild == None:
      self.leftChild = BinaryTree(newNode)

    # has left child
    else:
      t = BinaryTree(newNode)
      t.leftChild = self.leftChild
      self.leftChild = t


  def insertRight(self, newNode):
    # no right child
    if self.rightChild == None:
      self.rightChild = BinaryTree(newNode)

    # has right child
    else:
      t = BinaryTree(newNode)
      t.rightChild = self.rightChild
      self.rightChild = t

  def getRightChild(self):
    return self.rightChild

  def getLeftChild(self):
    return self.leftChild

  def setRootVal(self, obj):
    self.key = obj

  def getRootVal(self):
    return self.key

def preorder(tree):
  if tree:
    print(tree.getRootVal())
    preorder(tree.getLeftChild())
    preorder(tree.getRightChild())

def postorder(tree):
  if tree:
    preorder(tree.getLeftChild())
    preorder(tree.getRightChild())
    print(tree.getRootVal())

def inorder(tree):
  if tree:
    preorder(tree.getLeftChild())
    print(tree.getRootVal())
    preorder(tree.getRightChild())

# Priority Queues with Binary Heaps
# - queue with priorities

# in order to guarantee log performance, we must keep our tree balanced
  # balanced - roughly the same number of noes in left and right

class BinHeap:
  def __init__(self):
    self.heapList = [0]
    self.currentSize = 0

  def insert(k):
    self.heapList.append(k)
    self.currentSize = self.currentSize + 1
    self.percUp(self.currentSize)
  
  def percUp(self, i):
    while i // 2 > 0:
      if self.heapList[i] < self.heapList[ i // 2]:
        tmp = self.heapList[i // 2]
        self.heapList[i // 2] = self.heapList[i]
        self.heapList[i] = tmp
      i = i // 2
  
  def delMin(self):
    retval = self.heapList[1]
    self.heapList[1] = self.heapList[self.currentSize]
    self.currentSize = self.currentSize - 1
    self.heapList.pop()
    self.percDown(1)
    return retval

  def percDown(self, i):
    while (i * 2) <= self.currentSize:
      mc = self.minChild(i)
      if self.heapList[i] > self.heapList[mc]:
        tmp = self.heapList[i]
        self.heapList[i] = self.heapList[mc]
        self.heapList[mc] = tmp
      i = mc
    
  def minChild(self, i):
    if i * 2 + 1 > self.currentSize:
      return i * 2
    else:
      if self.heapList[i*2] < self.heapList[i*2+1]:
        return i * 2
      else:
        return i * 2 + 1
      
  def buildHeap(self, alist):
    i = len(alist) // 2
    self.currentSize = len(alist)
    self.heapList = [0] + alist[:]
    while (i > 0):
      self.percDown(i)
      i = i - 1

# BST
# keys < parent are in the left subtree
# keys > parent are in the left subtree
# depth first -> recursion
# breadth first -> queue

def is_bst_iter(tree):
  pass
  
def is_bst(iter):
  pass

class Node:
    def __init__(self, val=None):
        self.left = None
        self.right = None
        self.val =  val

def levelOrderPrint(tree):
  nodes = [(tree, 0)]

  depth_chart = {}
  cur_depth = 0
  while len(nodes) > 0:
    node, d = nodes.pop()
    if node.right:
      nodes.append((node.right, d+1))

    if node.left:
      nodes.append((node.left, d+1))
    
    if d in depth_chart:
      depth_chart[d].append(node.val)
    else:
      depth_chart[d] = [node.val]
  
  for n in range(len(depth_chart.keys())):
    print(" ".join([ str(x) for x in depth_chart[n]]))

n = Node(1)
l = n.left = Node(2)
r = n.right = Node(3)
l.left = Node(4)
r.left = Node(5)
r.right = Node(6)

print('Level Order Print')
levelOrderPrint(n)

def trimBST(tree,minVal,maxVal):
  if not tree:
    return

  tree.left = trimBST(tree.left, minVal, maxVal)
  tree.right = trimBST(tree.right, minVal, maxVal)

  print(tree.val)
  if minVal <= tree.val <= maxVal:
    return tree
  
  if tree.val < minVal:
    return tree.right

  if tree.val > maxVal:
    return tree.left

n = Node(8)
l = n.left = Node(3)
r = n.right = Node(10)
l.left = Node(1)
l1r1 = l.right = Node(6)
l1r1.right = Node(7)
l1r1.left = Node(4)

r2 = r.right = Node(14)
r2.left = Node(13)

print('Trim BST')
levelOrderPrint(n)
n = trimBST(n, 5, 13)
print('Trimmed BST')
levelOrderPrint(n)
