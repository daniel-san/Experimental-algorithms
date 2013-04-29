#! /usr/bin/env python
# -*- coding: utf8 -*-
import math
import random
class Node():
    def __init__(self,x,y):
        self.group = -1
        self.X = x
        self.Y = y
        self.visited = False
    
    
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
   
def create_adj_list(mst,nodes_number):
    ret_list = []
    for i in range(nodes_number):
	ret_list.append([])

    for n in mst:
	ret_list[n.n1.id].append(n.n2.id)
	ret_list[n.n2.id].append(n.n1.id)

    return ret_list

def HC_dfs(node,tree_adj,final_cycle,nodes):
    if not node.visited:
        final_cycle.append(node)
        node.visited = True
        for i in tree_adj[node.id]:
	    HC_dfs(nodes[i],tree_adj,final_cycle,nodes)
    
if __name__ == "__main__":
    n_total = input()
    
    graph = Graph()
    
    for i in range(0,n_total):
        node = Node(random.randint(0,1000),random.randint(0,1000))
        node.group = i
	node.id = i
        graph.nodes.append(node)
    
    for i in range(len(graph.nodes)):
        for j in range(i):
	    e = Edge(graph.nodes[i],graph.nodes[j])
	    e.calcPeso()
	    graph.edges.append(e)
    
    mst = mst_kruskal(graph)
    adj_list = create_adj_list(mst,len(graph.nodes))
    cycle = []
    HC_dfs(mst[0].n1,adj_list,cycle,graph.nodes)
    edges = []
    size = len(cycle)
    for i in range(size):
        if i+1 < size:
	    print "%s %s %s %s" % (cycle[i].X,cycle[i].Y,cycle[i+1].X,cycle[i+1].Y)
	    
    print "%s %s %s %s" % (cycle[i].X,cycle[i].Y,cycle[0].X,cycle[0].Y)

