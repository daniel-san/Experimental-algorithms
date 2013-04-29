#! /usr/bin/env python
# -*- coding: utf8 -*-
import math
import random
from copy import copy
from graph import Node
class A_Node(Node):
    def __init__(self,x,y):
        Node.__init__(self,x,y)
	self.id = None
        
    def calc_weight_between(self,node2):
        return math.sqrt((node2.X - self.X)**2 + (node2.Y - self.Y)**2)

class Chromosome():
    def __init__(self):
        self.topology = []
        self.nodes = []
        self.fitness = 0.0
        
    def start_topology(self,s):
        self.topology.append(-1)
        for i in range(1,s):
	    d = random.randint(0, i-1)
	    self.topology.append(d)

    def get_fitness(self):
	total = 0.0
        
        for i in range(1, len(self.nodes)):
            total += self.nodes[i].calc_weight_between(self.nodes[self.topology[i]])
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
	    
class Gen_MST():
    def __init__(self,size,pop):
        self.population_size = pop
        self.population = []
	self.next_population = []
	self.got_next_pop = False
	self.tam_chrom = size
        self.chromosome = Chromosome()
        self.chromosome.start_topology(size)
        self.best_fitness = 0.0
	self.biz_chance = 0.05
        self.mutant_chance = 0.01
        self.cross_chance = 0.7

    def gerar_pop(self):
        pop_nodes = []
        
	for i in range(0,self.tam_chrom):
	    a = A_Node(random.randint(0,1000),random.randint(0,1000))
	    a.id = i
            pop_nodes.append(a)

        for i in range(0,self.population_size):
            embryon = Chromosome()
            embryon.start_topology(self.tam_chrom)
            embryon.nodes = copy(pop_nodes)
	    embryon.set_fitness()
            self.population.append(embryon)
            random.shuffle(pop_nodes)

        self.calc_fitness()

    def select_parents(self):
	parent_number = 10
	parents = []
	roulette_list = []
#	victorious_pop = self.tournament(self.population,self.population_size/10)
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
#	if random.random() < self.biz_chance:
#	    victorious = self.tournament(victorious,len(victorious)/2)
	return victorious

    def calc_fitness(self):
        for i in self.population:
            if self.best_fitness == 0:
                 self.best_fitness = i.get_fitness()

            if self.best_fitness > i.get_fitness():
                 self.best_fitness = i.get_fitness()

    def c_over(self,p1,p2,spl):
        num = len(p1)
	return p1[:spl] + p2[spl:num]
        
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
            if not child[i]:
                child[i] = p2[i]

        return child

    def crossing(self,parents):
	childs = []
	p1 = parents[0]
	p2 = parents[1]
        if random.random() < self.cross_chance:
	    for i in range(2):
	        cross_topology = self.c_over(p1.topology,p2.topology,random.randint(0,len(p1.nodes)))

		child = Chromosome()
		child.topology = cross_topology
		child.nodes = self.crossing_nodes(p1.nodes,p2.nodes)
		child.set_fitness()
		childs.append(child)

		p1, p2 = p2, p1

	return childs

    def single_mutation(self,nodes):
        size = len(nodes) - 1
	trade1 = random.randint(0,size)
	trade2 = random.randint(0,size)

	nodes[trade1], nodes[trade2] = nodes[trade2], nodes[trade1]
	return nodes

    def mutation(self,childs):
        if random.random() < self.mutant_chance:
	    for i in childs:
                size = len(i.topology)
		ch = random.randint(1,size - 1)
		i.nodes = self.single_mutation(i.nodes)
		i.topology[ch] = random.randint(0,size-1)
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
               self.got_next_pop = True

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

	
    a = Gen_MST(10,100)
    a.finish_him(10,20000)
    a.population.sort()
    p = a.population[0]
    print 'Chromosome'
    node_number = len(p.topology)
    for i in range(1,node_number):
        p1, p2 = p.nodes[i], p.nodes[p.topology[i]]
        print '%s %s %s %s' % (p1.X, p1.Y, p2.X, p2.Y) 



