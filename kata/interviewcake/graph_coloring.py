# Given an undirected graph with maximum degree D, find a graph coloring using at most D+1 colors.

class GraphNode:

def __init__(self, label):
  self.label = label
  self.neighbors = set()
  self.color = None

a = GraphNode('a')
b = GraphNode('b')
c = GraphNode('c')

a.neighbors.add(b)
b.neighbors.add(a)
b.neighbors.add(c)
c.neighbors.add(b)

graph = [a, b, c]

