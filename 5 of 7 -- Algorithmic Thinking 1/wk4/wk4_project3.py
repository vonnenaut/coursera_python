"""
wk4_project3.py

Provided code for Application portion of Module 2
"""

# general imports
import urllib2
import random
import time
import math
import UPATrial

# CodeSkulptor import
#import simpleplot
#import codeskulptor
#codeskulptor.set_timeout(60)

# Desktop imports
import matplotlib.pyplot as plt


############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order
    


##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph


def gen_er_graph(num_nodes, probability):
	""" pseudocode:
	algorithm for generating random undirected graphs (ER graphs)
	Algorithm 1:  ER
	Input: Number of nodes n; probability p,
	Output:  A graph g = (V, E) where g is an element of G(n, p)
  	1  V <-- {0, 1, ... n-1};
  	2  E <-- null;
  	3  foreach {i, j} that is a unique element of V, where i is not j do
  	4      a <-- random(0, 1);    // a is a random real number in [0, 1)
  	5      if a < p then
  	6          E <-- E union {{i, j}};
  	7  return g = (V, E)
  	"""
	if num_nodes <= 0:
	 	return {}
  	graph = {}   	
  	for node in range(num_nodes):
  		E = set()	# edges
  		for neighbor in range(num_nodes):
  			a = random.random() 
  			# print "a:", a 			
  			if node != neighbor and a < probability:
  				E.add(neighbor)
  		graph[node] = E

  	# print "graph:", graph
  	return graph


def gen_upa_graph(final_nodes, num_nodes):
	""" 
	generates a random undirected graph iteratively, where in each iteration a new node is created and added to the graph, connected to a subset of the existing nodes.  The subset is chosen based on in-degrees of existing nodes. 

	n: final_nodes
	m: num_nodes
	"""
	# create complete directed graph on m nodes (num_nodes)
	graph = make_complete_graph(num_nodes)

	V = []
	E = []
	total_indeg = 0

	for key in graph:
		V.append(key)
		E.append([key,graph[key]])	

	# grow the graph by adding n - m (final_nodes - num_nodes) nodes
	# where each new node is connected to m nodes randomly chosen 
	# from the set of existing nodes.  Elimintate duplicates 
	# to avoid parallel edges.
	for node_added in range(num_nodes, final_nodes):
		# for key in graph:
		# 	for value in graph[key]:
		# 		total_indeg += value
		V_prime = set()
		# choose randomly m nodes from V and add them to V_prime 
		# where the probability of choosing node j is (indeg(j) + 1)/(totindeg + |V|)
		# i.e., call DPATrial (line 6 in pseudocode)
		trial = UPATrial.UPATrial(num_nodes)
		V_prime = trial.run_trial(num_nodes)
		for node in V_prime:
			V_prime.add(node)
		V.append(node_added)
		graph[node_added] = V_prime
	return graph