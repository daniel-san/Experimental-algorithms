#! /usr/bin/env python
# -*- coding: utf8 -*-
import math
import random
import node_file
import sys
from copy import copy
from graph import Node
class A_Node(Node):
    def __init__(self,x,y):
        Node.__init__(self,x,y)
	self.id = None
        
    def calc_weight_between(self,node2):
        return math.sqrt((node2.X - self.X)**2 + (node2.Y - self.Y)**2)

class Chromosome():
        
    def __init__(self,nodes=[],nodes_id=[]):
        self.nodes = nodes
        self.nodes_id = nodes_id
        self.fitness = 0.0
   
 
    def get_fitness(self):
	total = 0.0
        nodes_number = len(self.nodes_id)

        for i in range(nodes_number):
            id = self.nodes_id[i]
            next_id = self.nodes_id[(i + 1) % nodes_number]
            start = self.nodes[id]
            finish = self.nodes[next_id]
            total += start.calc_weight_between(finish)
        return total

    def set_fitness(self):
         self.fitness = self.get_fitness()

    def __cmp__(self,other):
        if self.fitness < other.fitness:
	    return -1
	elif self.fitness > other.fitness:
	    return 1
	else:
	    return 0
	    
class Gen_TSP():
    def __init__(self,size,nodes):
        self.population_size = size
        self.population = []
	self.next_population = []
	
	self.nodes = nodes
	self.tam_chrom = len(self.nodes)

        self.best_fitness = -1
        self.mutant_chance = 0.01
        self.cross_chance = 0.7

    def gerar_pop(self):
        ids = range(self.tam_chrom)
        random.shuffle(ids)

        for i in range(self.population_size):
            embryon = Chromosome(self.nodes,copy(ids))
	    embryon.set_fitness()
	    if self.best_fitness == -1:
	        self.best_fitness = embryon.fitness
	    elif embryon.fitness < self.best_fitness:
	        self.best_fitness = embryon.fitness
	    
            self.population.append(embryon)
            random.shuffle(ids)

    def select_parents(self):
	parent_number = 10
	parents = []
	roulette_list = []
        victorious_pop = self.population
	max_fitness = 0.0
	for c in victorious_pop:
            total = c.get_fitness()
	    if total > max_fitness:
		max_fitness = total

	total_fitness = 0.0
	min_value = 0.0
	for c in victorious_pop:
	    fitness = max_fitness - c.fitness + 1
	    total_fitness += fitness

	for c in victorious_pop:
	    fitness = max_fitness - c.fitness + 1
	    probability = float(fitness) / total_fitness
	    roulette_list.append((min_value, min_value + probability))
	    min_value += probability

	for i in range(parent_number):
	    selected_slice = self.selected_rs(random.random(),roulette_list)

	    parents.append(selected_slice)

        
	return self.tournament(parents,2)

    def selected_rs(self,choice,r_list):
        for i in range(len(r_list)):
	    if choice>= r_list[i][0] and choice < r_list[i][1]:
	        return self.population[i]

    def tournament(self,population, tournament_size):
	victorious = []
	pop = copy(population)
	while len(victorious) < tournament_size and len(population) > 1:
	    random.shuffle(pop)
	    tournament_grounds = pop[:tournament_size]
	    tournament_grounds.sort()
	    victorious.append(tournament_grounds[0])
	return victorious

    def calc_fitness(self):
        for i in self.population:
            if self.best_fitness == 0:
                 self.best_fitness = i.get_fitness()

            if self.best_fitness > i.get_fitness():
                 self.best_fitness = i.get_fitness()

        
    def crossing_nodes(self,p1,p2):
        gene_num = len(p1)
        child = []
	for i in range(gene_num):
	    child.append(None)

        i = 0
        have_cycle = False
        while not have_cycle:
            child[i] = p1[i]
            gene = p2[i]
            i = p1.index(gene)

            if p1[i] in child:
                have_cycle = True

        for i in range(gene_num):
            if child[i] == None:
                child[i] = p2[i]

        return child

    def crossing(self,parents):
	childs = []
	p1 = parents[0]
	p2 = parents[1]
        if random.random() < self.cross_chance:
	    for i in range(2):
		child = Chromosome()
		child.nodes_id = self.crossing_nodes(p1.nodes_id,p2.nodes_id)
		child.nodes = self.nodes
		child.set_fitness()
		childs.append(child)

		p1, p2 = p2, p1

	return childs

    def single_mutation(self,node_ids):
        size = len(node_ids) - 1
	trade1 = random.randint(0,size)
	trade2 = random.randint(0,size)

	node_ids[trade1], node_ids[trade2] = node_ids[trade2], node_ids[trade1]
	return node_ids

    def mutation(self,childs):
        if random.random() < self.mutant_chance:
	    for i in childs:
		i.nodes_id = self.single_mutation(i.nodes_id)
		i.set_fitness()
	return childs

    def generate_next_population(self,childs):
	if childs:
           got_new_pop = False
	   for c in childs:
	       if len(self.next_population) < self.population_size:
                   if c.fitness < self.best_fitness:
                       self.next_population.append(c)
               else:
                   got_new_pop = True
           if got_new_pop:
               self.population = self.next_population
               self.next_population = []
               self.calc_fitness()


    def	finish_him(self,min_fitness,generations):
        current_generation = 1
        self.gerar_pop()
	while self.best_fitness > min_fitness and current_generation <= generations:
	    print '\rCurrent Generation : %s Best Fitness %s' % (current_generation,self.best_fitness),
            parents = self.select_parents()
            cross_result = self.crossing(parents)
            if cross_result:
                new_child = self.mutation(cross_result)
                self.generate_next_population(new_child)
		self.calc_fitness()
            current_generation += 1

if __name__ == "__main__":
    nodes = []
    if len(sys.argv) == 2:
        nodes_coords = node_file.load(sys.argv[1])

        for i in range(len(nodes_coords)):
	    node = A_Node(nodes_coords[i][0],nodes_coords[i][1])
	    node.id = i
	    nodes.append(node) 
    else:
        n_total = input()
	for i in range(n_total):
	    n = A_Node(random.randint(0,1000),random.randint(0,1000))
	    n.id = i
	    nodes.append(n)
	    
    a = Gen_TSP(100,nodes)
    a.finish_him(10,10000)
    a.population.sort()
    p = a.population[0]
    for i in range(len(p.nodes)):
        if i+1 < len(p.nodes):
	    print "%s %s %s %s" % (p.nodes[i].X,p.nodes[i].Y,p.nodes[i+1].X,p.nodes[i+1].Y)
	    
    print "%s %s %s %s" % (p.nodes[i].X,p.nodes[i].Y,p.nodes[0].X,p.nodes[0].Y)


