#! /usr/bin/env python
# -*- coding: utf8 -*-
import math
import random
from node_file import load
class Node():
    def __init__(self,x,y):
        self.group = -1
        self.X = x
        self.Y = y
    
    
class Edge():
    def __init__(self,n1,n2):
        self.n1 = n1
        self.n2 = n2
        self.peso = None
        
    def calcPeso(self):
	self.peso = math.sqrt((self.n2.X - self.n1.X)**2 + (self.n2.Y - self.n1.Y)**2)
	
    def __cmp__(self,other):
        if self.peso < other.peso:
	    return -1
	elif self.peso > other.peso:
	    return 1
	else:
	    return 0
	
class Graph():
    def __init__(self):
        self.nodes = []
        self.edges = []
        
        
def mst_kruskal(graph):
    mst = []
    arestas = graph.edges
    arestas.sort()
    
    edge_counter = 0
    
    while len(mst) < len(graph.nodes) -1:
        e = arestas[edge_counter]
        if e.n1.group != e.n2.group:
            n1_g = e.n1.group
            n2_g = e.n2.group
            for n in graph.nodes:
                if n2_g == n.group:
                    n.group = n1_g
                    
            mst.append(e)  
	edge_counter += 1
	
    return mst
    
    
if __name__ == "__main__":
#    n_total = input()
    file_name = raw_input("File Name:")
    nodes = load(file_name)
    graph = Graph()
    
#    for i in range(0,n_total):
#        node = Node(random.randint(0,1000),random.randint(0,1000))
#        node.group = i
#        graph.nodes.append(node)
    for i in range(0,len(nodes)):
	    a = Node(nodes[i][0],nodes[i][1])
	    a.group = i
            graph.nodes.append(a)
    
    for i in range(len(graph.nodes)):
        for j in range(i):
	    e = Edge(graph.nodes[i],graph.nodes[j])
	    e.calcPeso()
	    graph.edges.append(e)
    
    mst = mst_kruskal(graph)
    
    fitness = 0.0
    for i in mst:
	fitness += i.peso
        print "%s %s %s %s" % (i.n1.X, i.n1.Y, i.n2.X, i.n2.Y)

    print fitness
#    for i in graph.nodes:
#	print "%s %s" % (i.X, i.Y)
    
