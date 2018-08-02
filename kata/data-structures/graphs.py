
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

class Vertex:
    def __init__(self,key):
        self.id = key
        self.connectedTo = {}

    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self,nbr):
        return self.connectedTo[nbr]

class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self,f,t,cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())

g = Graph()
for i in range(6):
    g.addVertex(i)

g.vertList
g.addEdge(0,1,2)
for vertex in g:
    print(vertex)
    for c in vertex.getConnections():
        print('weight', vertex.getWeight(c))

# Word ladder problem
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

words = ['pope', 'rope', 'sage', 'best', 'ripe', 'pipe']
buildGraph(words)

# breadth first search
# finds all k veriticies before k+1



# knights tour
# represent the legal moves of the knight on a chessboard
#** for larger graphs the adjancy matrix is the way to go