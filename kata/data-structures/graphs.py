
# graphs are a more general structure than trees (trees are a type of graph)
# graph has nodes (vertex), keys (name/payload), and edges
# edges may be weighted to show the cost of  moving between nodes
# edges may be one way or two way

# Directed graph (digraph) -> all the edges in a graph are all one-way

# For the graph G, V is a set of vertices and E is a set of edges
# G=(V,E)
# V = set of verticies
# # = set of edges
# e and v and subsets

# each edge is a tuple (v,w) where w,v(element of V)
# weight

# Path -> sequence of verticies connected by edges
# Cycle -> path that starts and ends at the same vertex
# A graph with no cycles is called an acyclic graph
# A directed graph with no cycles is called a DAG (directed acyclic graph)

# Adjacency Matrix
# each of the rows and columns represent a vertex in the graph
# good implementation for a graph when the number of edges is large
# the number of edges required to fill the matirx is |V|^2
# a matrix is full when every vertex is connected to every other vertex

# Adjacency List
# A more space efficient way to represent a sparsely connected graph

# Implement Graph
from enum import Enum
from collections import OrderedDict

class State(Enum):
    unvisited = 1   # White
    visited = 2     # Black
    visiting = 3    # Gray

class Node:

    def __init__(self, num):
        self.num = num
        self.visit_state = State.unvisited
        self.adjacent = OrderedDict()  # key = node, val = weight

    def __str__(self):
        return str(self.num)

class Graph:

    def __init__(self):
        self.nodes = OrderedDict()  # key = node id, val = node

    def add_node(self, num):
        node = Node(num)
        self.nodes[num] = node
        return node

    def add_edge(self, source, dest, weight=0):
        if source not in self.nodes:
            self.add_node(source)
        if dest not in self.nodes:
            self.add_node(dest)
        self.nodes[source].adjacent[self.nodes[dest]] = weight


# Implement Depth First Search

def dfs(graph, start):
  visited, stack = set(), [start]

  while stack:
    vertex = stack.pop()
    print(vertex)

    if vertex not in visited:
      visited.add(vertex)
      stack.extend(graph[vertex] - visited)

  return visited

def bfs(graph, start):
  visited, queue = set(), [start]

  while queue:
    vertex = queue.pop(0)
    print(vertex)

    if vertex not in visited:
      visited.add(vertex)
      queue.extend(graph[vertex] - visited)

  return visited


graph = { 'A': set(['B', 'C']),
          'B': set(['A', 'D', 'E']),
          'C': set(['A', 'F']),
          'D': set(['B']),
          'E': set(['B', 'F']),
          'F': set(['C', 'E'])}


print('DFS')
print(dfs(graph, 'A'))


print('BFS')
bfs(graph, 'A')

# Word ladder problem

# breadth first search -> QUEUE
# finds all k veriticies before k+1

def buildGraph(word):
    d = {}
    g = Graph()
    
    # create buckets of words that differ by one letter
    for line in words:
        print(line)
        word = line[:-1]
        print(word)
        for i in range(len(word)):
            bucket = word[:i] + '_' + word[i+1:]
            if bucket in d:
                d[bucket].append(word)
            else:
                d[bucket] = [word]
    # add vertices and edges for words in the same bucket
    for bucket in d.keys():
        for word1 in d[bucket]:
            for word2 in d[bucket]:
                if word1 != word2:
                    g.addEdge(word1,word2)
    return g

# words = ['pope', 'rope', 'sage', 'best', 'ripe', 'pipe']
# buildGraph(words)

# knights tour
# represent the legal moves of the knight on a chessboard
#** for larger graphs the adjancy matrix is the way to go

# depth first search -> STACK
# 
