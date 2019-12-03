"""
Aplication #2

Questions
"""
# general imports
import urllib2
import random
import time
import math
import UPATrial
import numpy
import poc_simpletest as test
from collections import deque
import matplotlib.patches as mpatches

# CodeSkulptor import
#import simpleplot
#import codeskulptor
#codeskulptor.set_timeout(60)

# Desktop imports
import matplotlib.pyplot as plt


############################################
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
    	if neighbor in ugraph and node in ugraph[neighbor]:
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
        	if neighbor in new_graph and max_degree_node in new_graph[neighbor]:
        		new_graph[neighbor].remove(max_degree_node)
        order.append(max_degree_node)
    return order
    
def print_iterable(iterable):
	for line in iterable:
		print line
	print

def fast_targeted_order(ugraph):
	""" a faster version of targeted_order --
	Creates a list degree_sets whose kth element is the set of nodes of degree k. The method then iterates through the list degree_sets in order of decreasing degree. When it encounters a non-empty set, the nodes in this set must be of maximum degree. The method then repeatedly chooses a node from this set, deletes that node from the graph, and updates degree_sets appropriately.

	Returns a list of the nodes in ugraph in decreasing order of their degrees."""
	new_graph = copy_graph(ugraph)
	# print "new_graph:", new_graph
	graph_size = len(new_graph)
	# initialize degree_sets as a list of empty sets
	degree_sets = []
	for index in range(graph_size):
		degree_sets.append(set([]))

	# populate list with nodes which have corresponding indexed number of degrees
 	for node in range(graph_size):
		if node in new_graph:
			degree = len(new_graph[node])
			degree_sets[degree].add(node)

	# Testing code ---------------------
	# The following lines are for tests 1 and 2:
	# print "degree_sets:", degree_sets
	# return degree_sets
	# End testing code -----------------

	ordered_list = []
	incr = 0

	# iterate through degree_sets in reverse order
	# and arrange them in descending order based on number of degrees
	for index in range(len(degree_sets)-1, -1, -1):
		# print "\nindex:", index
		# print "len(degree_sets[%r]): %r" % (node, len(degree_sets[node]))
		while len(degree_sets[index]) > 0:
		# When it encounters a non-empty set, the nodes in this set must be of maximum degree. The method then repeatedly chooses a node from this set, deletes that node from the graph, and updates degree_sets appropriately.
			arbitrary_node = random.sample(degree_sets[index], 1)
			arbitrary_node = int(arbitrary_node[0])
			# print "arbitrary_node:", arbitrary_node
			# print "new_graph[index]:", new_graph[index]
			if index in new_graph and arbitrary_node in new_graph[index]:
				# print "degree_sets[index]:", degree_sets[index]
				# print "new_graph[degree_sets[arbitrary_node]]:", new_graph[arbitrary_node]
				for neighbor in new_graph[arbitrary_node]:
					# print "neighbor:", neighbor
					if neighbor in new_graph and arbitrary_node in new_graph[neighbor]:
						new_graph[neighbor].remove(arbitrary_node)
				del new_graph[arbitrary_node]
			if arbitrary_node in degree_sets[index]:
				degree_sets[index].remove(arbitrary_node)
			ordered_list.append(arbitrary_node)
			# print "new_graph:", new_graph
			# print "degree_sets:", degree_sets
			# print "ordered_list:", ordered_list
	return ordered_list


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


def make_complete_graph(num_nodes):
	"""
	Takes the number of nodes num_nodes and returns a dictionary corresponding to a complete directed graph with the specified number of nodes. A complete graph contains all possible edges subject to the restriction that self-loops are not allowed. 
	"""
	if num_nodes <= 0:
		return {}
	dict_graph = {}
	for node in range(num_nodes):
		node_set = set()
		for neighbor in range(num_nodes):
			if node != neighbor:
				node_set.add(neighbor)
		dict_graph[node] = node_set

	return dict_graph


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
  		node_set = set()	# edges
  		for neighbor in range(num_nodes):
  			random_value = random.random() 
  			# print "a:", a 			
  			if node != neighbor and random_value < probability:
  				node_set.add(neighbor)
  		graph[node] = node_set

  	# print "graph:", graph
  	return graph


def gen_upa_graph(final_nodes, num_nodes, probability):
	""" 
	generates a random undirected graph iteratively, where in each iteration a new node is created and added to the graph, connected to a subset of the existing nodes.  The subset is chosen based on in-degrees of existing nodes. 
	n: final_nodes
	m: num_nodes
	"""
	if num_nodes > final_nodes or final_nodes < 1:
		return {}
		
	# create random undirected graph on m nodes (num_nodes)
	graph = gen_er_graph(num_nodes, probability)

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

def random_order(graph):
	""" returns a list of nodes in the graph in a random order """
	keys_list = []

	for key in graph:
		keys_list.append(key)
	random.shuffle(keys_list)
	return keys_list


def test_random_order():
	""" tests random_order function """
	graph = {0: {1, 2},
			 1: {0},
			 2: {0},
			 3: {4},
			 4: {3}}

	print "graph:", graph
	ro_graph = random_order(graph)
	print "random_order graph:", ro_graph


def bfs_visited(ugraph, start_node):
	""" takes undirected graph and node as input;
	returns set of all nodes visited by breadth-first search starting at start_node """
	queue = deque()
	visited = set([start_node])

	queue.append(start_node)
	# print "start_node:", start_node

	while len(queue) > 0:
		current_node = queue.pop()
		# print "current_node:", current_node
		if current_node in ugraph:
			for neighbor in ugraph[current_node]:
				if neighbor not in visited:
					visited.add(neighbor)
					queue.append(neighbor)
	return visited


def cc_visited(ugraph):
	""" takes ugraph and returns list of sets where each set consists of all the nodes (and nothing else) in a connected component and there is exactly one set in the list for each connected component in ugraph and nothing else
	"""
	remaining_nodes = []

	for node in ugraph:
		remaining_nodes.append(node)
	c_comp = []

	while len(remaining_nodes) > 0:
		current_node = remaining_nodes.pop()
		working_set = bfs_visited(ugraph, current_node)
		c_comp.append(working_set)
		dummyvar = [remaining_nodes.remove(ws_item) for ws_item in working_set if ws_item in remaining_nodes]
	return c_comp


def largest_cc_size(ugraph):
	""" computes and returns the size of the largest connected component of ugraph; returns an int """
	largest_num = 0
	c_comp = cc_visited(ugraph)

	for group in c_comp:
		if len(group) > largest_num:
			largest_num = len(group)
	return largest_num


def compute_resilience(ugraph, attack_order):
	""" takes an undirected graph and a list of nodes, attack_order;
	iterates through the nodes in attack_order.
	For each node, removes the given node and its edges from ugraph and then computes the size of the largest cc for the resulting graph.  
	returns a list whose k + 1th entry is the size of the largest cc in the graph after removal of the first k nodes in attack_order.  The first entry in the returned list is the size of the largest cc in the original graph"""
	resilience = []
	resilience.append(largest_cc_size(ugraph))
	# iterate through nodes in attack_order
	for target in attack_order:
		# in order to remove given node and its edges from ugraph
		# first create a list of neighbor nodes to visit for removal of edges
		neighbors = bfs_visited(ugraph, target)
		# then visit each neighbor, removing target from its list of neighbors
		for neighbor in neighbors:
			if neighbor in ugraph and target in ugraph[neighbor]:
				ugraph[neighbor].remove(target)
				# delete_node(ugraph, target)
		# next remove the target node
		# del ugraph[target]
		delete_node(ugraph, target)
		# compute size of largest cc for resulting graph
		largest_cc = largest_cc_size(ugraph)
		# append largest cc to result list
		resilience.append(largest_cc)

	# return result list
	# print "\nresilience:", resilience
	return resilience

# Begin Tests -------------------------------------
def run_suite():
    """
    Some informal testing code
    """
    # create a TestSuite object
    suite = test.TestSuite()

    def network_analysis():
    	""" Question 4:
    	"""
    	# A.  compute a targeted attack order for each of the three graphs (computer network, ER, UPA) from Question 1
    	# B. compute the resilience of each graph
    	# C. plot the computed resiliences as three curves (line plots) on a single plot.  NOTE: The text labels in this legend should include the values for p and m that you used in computing the ER and UPA graphs, respectively.
    	probability = .004
    	num_nodes = 1200
    	final_nodes = 1239

    	# network ------------------
    	network_graph = load_graph(NETWORK_URL)
    	attack_order_net = fast_targeted_order(network_graph)
    	resilience_net = compute_resilience(network_graph, attack_order_net)

    	# ER -----------------------
    	er_graph = gen_er_graph(num_nodes, probability)
    	attack_order_er = fast_targeted_order(er_graph)
    	resilience_er = compute_resilience(er_graph, attack_order_er)

    	# UPA ----------------------
    	upa_graph = gen_upa_graph(final_nodes, num_nodes, probability)
    	attack_order_upa = fast_targeted_order(upa_graph)
    	resilience_upa = compute_resilience(upa_graph, attack_order_upa)

    	# plot all three resilience curves on a single standard plot
    	xvals = range(num_nodes)
    	xvals = range(len(resilience_net))
    	xvals2 = range(len(resilience_er))
    	xvals3 = range(len(resilience_upa))
    	yvals1 = resilience_net
    	yvals2 = resilience_er
    	yvals3 = resilience_upa
    	
    	plt.plot(xvals, yvals1, '-b', label='Network')
    	plt.plot(xvals2, yvals2, '-r', label='ER  p = 0.004')
    	plt.plot(xvals3, yvals3, '-g', label='UPA  m = 1200')
    	plt.xlabel('number of nodes removed')
    	plt.ylabel('resilience')
    	# p_value = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
    	# m_value = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
    	# plt.legend([extra, bar_0_10, bar_10_100], ("My explanatory text", "0-10", "10-100"))
    	# plt.legend([p_value, m_value, net_leg, er_leg, upa_leg], ("p =" + str(probability), "\nm = " + str(num_nodes), "Network", "ER", "UPA", loc='upper right'))
    	plt.legend(loc='upper right')
    	p_m_label = "p = %r \n m = %r" % (probability, num_nodes)
    	handles, labels = plt.get_legend_handles_labels()
    	handles.append(mpatches.Patch(color='none', label=p_m_label))
    	plt.legend(handles=handles)
    	plt.show()

    def analyze_methods():
 		""" Question 3:  comparatively analyzes run times of targeted_order and fast_targeted_order methods """
 		# Big-O bounds:
 		# targeted_order:
 		# n^2 + 5n
 		# fast_targeted_order:
 		# 3n
 		ugraph1 = {0: {1, 2},
				  1: {0},
				  2: {0}}
				  
		ugraph2 = {0: {1, 2},
				  1: {0},
				  2: {0},
				  3: {4, 5, 6},
				  4: {3, 5},
				  5: {3, 4},
				  6: {3},
				  7: {8},
				  8: {7},
				  9: {}} 

		ugraphs = [ugraph1, ugraph2]
		upa_graphs = []
		to_times = []
		fto_times = []

		# generate upa graphs for testing
		for n in range(10, 1000, 10):
			upa_graphs.append(gen_upa_graph(n, 5, .004))

 		# measure run time of targeted_order
		for graph in upa_graphs:
			start_time_to = time.time()
			targeted_order(graph)
			elapsed_time_to = time.time() - start_time_to
			to_times.append(elapsed_time_to)

		# measure run time of fast_targeted_order
		for graph in upa_graphs:
			start_time_fto = time.time()
			fast_targeted_order(graph)
			elapsed_time_fto = time.time() - start_time_fto
			fto_times.append(elapsed_time_fto)

		print "-------------------------------------------"
		to_total = 0
		for value in to_times:
			to_total += value
		print "targeted_order elapsed_time:", to_total
		fto_total = 0
		for value in fto_times:
			fto_total += value 
		print "fast_targeted_order elapsed_time:", fto_total

		# plot n(x) vs time (y) on a standard plot
		xvals = range(10, 1000, 10)
		yvals1 = to_times
		yvals2 = fto_times

		plt.plot(xvals, yvals1, '-b', label='targeted_order')
		plt.plot(xvals, yvals2, '-r', label='fast_targeted_order')
		plt.xlabel('number of nodes (n)')
		plt.ylabel('method running time')
		plt.legend(loc='upper right')
		plt.show()

  #   def test_fast_targeted_order():
		# """ tests degree_sets creation in fast_targeted_order
		# """	
		# ugraph1 = {0: {1, 2},
		# 		  1: {0},
		# 		  2: {0}}

		# ugraph2 = {0: {1, 2},
		# 		  1: {0},
		# 		  2: {0},
		# 		  3: {4, 5, 6},
		# 		  4: {3, 5},
		# 		  5: {3, 4},
		# 		  6: {3},
		# 		  7: {8},
		# 		  8: {7},
		# 		  9: {}} 

		# # NOTE:  uncomment lines labeled for tests 1 and 2 in fast_targeted_order to run the first 2 tests
		# # suite.run_test(fast_targeted_order(ugraph1), [set([]), set([1, 2]), set([0])], "Test #1:") 
		# # suite.run_test(fast_targeted_order(ugraph2), [set([9]), set([1, 2, 6, 7, 8]), set([0, 4, 5]), set([3]), set([]), set([]), set([]), set([]), set([]), set([])], "Test #2:")
		# print "\n\n------------------------------"
		# print "\n\nTesting fast_targeted_order ...\n"
		# suite.run_test(fast_targeted_order(ugraph1), [0, 1, 2], "Test #3:") 
		# suite.run_test(fast_targeted_order(ugraph2), [3, 0, 4, 7, 1, 2, 5, 6, 8, 9], "Test #4:") 
		# print "\n\n------------------------------"
		# print "\n\nTesting targeted_order ...\n" 
		# suite.run_test(targeted_order(ugraph1), [0, 2, 1], "Test #5")
 	# 	suite.run_test(targeted_order(ugraph2), [3, 0, 4, 7, 1, 2, 5, 6, 8, 9], "Test #6")

    # test_fast_targeted_order()
    # analyze_methods()
    network_analysis()
    suite.report_results()

run_suite()
# End Tests ---------------------------------------


# Questions---------------------------------------------
# 1.  probability = .004 m = 2 (# edges) 
# probability = .004
# num_nodes = 1200
# final_nodes = 1239
# for each of the 3 graphs, compute a random attack order using random_order and use this attack order in compute_resilience to compute the resilience of each graph
# # network ------------------
# network_graph = load_graph(NETWORK_URL)
# attack_order_net = random_order(network_graph)
# resilience_net = compute_resilience(network_graph, attack_order_net)
# # ER -----------------------
# er_graph = gen_er_graph(num_nodes, probability)
# attack_order_er = random_order(er_graph)
# resilience_er = compute_resilience(er_graph, attack_order_er)
# # # UPA ----------------------
# upa_graph = gen_upa_graph(final_nodes, num_nodes, probability)
# attack_order_upa = random_order(upa_graph)
# resilience_upa = compute_resilience(upa_graph, attack_order_upa)

# # plot all three resilience curves on a single standard plot (not log/log)
# xvals = range(num_nodes)
# xvals = range(len(resilience_net))
# xvals2 = range(len(resilience_er))
# xvals3 = range(len(resilience_upa))
# yvals1 = resilience_net
# yvals2 = resilience_er
# yvals3 = resilience_upa

# plt.plot(xvals, yvals1, '-b', label='Network')
# plt.plot(xvals2, yvals2, '-r', label='ER')
# plt.plot(xvals3, yvals3, '-g', label='UPA')
# plt.xlabel('number of nodes removed')
# plt.ylabel('resilience')
# plt.legend(loc='upper right')
# plt.show()

# ---------------------------
# 2.  All three graphs are resilient during attack as the first 20% of their nodes are removed.

"""
Question 2 (1 pt)

Consider removing a significant fraction of the nodes in each graph using random_order. We will say that a graph isresilientunder this type of attack if the size of its largest connected component is roughly (within ~25%) equal to the number of nodes remaining, after the removal of each node during the attack.

Examine the shape of the three curves from your plot in Question 1. Which of the three graphs are resilient under random attacks as the first 20% of their nodes are removed? Note that there is no need to compare the three curves against each other in your answer to this question.



"""

# --------------------------
# 3.  # Big-O bounds:
 		# targeted_order:
 		# n^2 + 5n
 		# fast_targeted_order:
 		# 3n


"""
Question 3 (3 pts)

In the next three problems, we will consider attack orders in which the nodes being removed are chosen based on the structure of the graph. A simple rule for thesetargeted attacks is to always remove a node of maximum (highest) degree from the graph. The function targeted_order(ugraph) in the provided code takes an undirected graph ugraph and iteratively does the following:

Computes a node of the maximum degree in ugraph. If multiple nodes have the maximum degree, it chooses any of them (arbitrarily).
Removes that node (and its incident edges) from ugraph.
Observe that targeted_order continuously updates ugraph and always computes a node of maximum degree with respect to this updated graph. The output of targeted_order is a sequence of nodes that can be used as input to compute_resilience.

As you examine the code for targeted_order, you feel that the provided implementation of targeted_order is not as efficient as possible. In particular, much work is being repeated during the location of nodes with the maximum degree. In this question, we will consider an alternative method (which we will refer to as fast_targeted_order) for computing the same targeted attack order. Here is a pseudo-code description of the method [ ... ]


4.  

To continue our analysis of the computer network, we will examine its resilience under an attack in which servers are chosen based on their connectivity. We will again compare the resilience of the network to the resilience of ER and UPA graphs of similar size.

Using targeted_order (or fast_targeted_order), your task is to compute a targeted attack order for each of the three graphs (computer network, ER, UPA) from Question 1. Then, for each of these three graphs, compute the resilience of the graph using compute_resilience. Finally, plot the computed resiliences as three curves (line plots) in a single standard plot. As in Question 1, please include a legend in your plot that distinguishes the three plots. The text labels in this legend should include the values for p and m that you used in computing the ER and UPA graphs, respectively.

Once you are satisfied with your plot, upload your plot into the peer assessment. Your plot will be assessed based on the answers to the following three questions:

Does the plot follow the formatting guidelines for plots?
Does the plot include a legend? Does this legend indicate the values for p and m used in ER and UPA, respectively?
Do the three curves in the plot have the correct shape?


5.  Which of the three graphs are resilient under targeted attacks as the first 20% of their nodes are removed? 
ER and UPA

Again, note that there is no need to compare the three curves against each other in your answer to this question.


6.  Theoretically, following a random design would increase network resilience but it's likely impractical in terms of network security and practical network topological design, which might lead to greater likelihood of malevolent/unwarranted network access in the first place, making irrelevant the overall increased resilience.  


"""