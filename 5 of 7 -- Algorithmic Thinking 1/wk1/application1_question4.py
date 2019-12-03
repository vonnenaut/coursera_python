"""
Application 1
Question 3
DPA algorithm
"""
"""
Application portion of Module 1
"""
# general imports
import urllib2
# Set timeout for CodeSkulptor if necessary
# import codeskulptor
# codeskulptor.set_timeout(20)
# import simpleplot
import matplotlib.pyplot as plt
import numpy as np
import random
import DPATrial

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

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
    
    # print "Loaded graph with", len(graph_lines), "nodes"
    
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


def compute_in_degrees(digraph):
	"""
	Takes a directed graph digraph (represented as a dictionary) and computes the in-degrees for the nodes in the graph. The function should return a dictionary with the same set of keys (nodes) as digraph whose corresponding values are the number of edges whose head matches a particular node.

	{0: set([1, 2]),
	 1: set([0, 2]),
	 2: set([0, 1])}
	"""

	in_degrees = {}

	for node in digraph:
		in_degrees[node] = 0

	for node in digraph:
		# print "node:", node
		for element in digraph[node]:
			# print "element:", element
			if element in digraph:
				# print "element in digraph:", element, digraph, element in digraph
				in_degrees[element] += 1

	# print "in_degrees:", in_degrees
	return in_degrees


def in_degree_distribution(digraph):
	"""
	Takes a directed graph digraph (represented as a dictionary) and computes the unnormalized distribution of the in-degrees of the graph. The function should return a dictionary whose keys correspond to in-degrees of nodes in the graph. 
	"""
	dist_in_degree = {}
	zero_in_count = 0
	node_indegs = compute_in_degrees(digraph)

	# now that we have our temp list of key-value pairs, let's consolidate any with the same key so as to not have duplicates
	for key in node_indegs:
		if node_indegs[key] not in dist_in_degree:
			dist_in_degree[node_indegs[key]] = 1
		elif node_indegs[key] in dist_in_degree:
			dist_in_degree[node_indegs[key]] += 1

	# Finally, let's add a count for nodes with zero in-degrees before creating our final dictionary and returning it
	for node in node_indegs:
		if node_indegs[node] == 0:
			zero_in_count += 1
	if zero_in_count > 0:
		dist_in_degree[0] = zero_in_count

	return dist_in_degree

def gen_random_graph(num_nodes, probability):
	""" pseudocode:
	algorithm for generating random undirected graphs
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

def dict_to_coord_lists(dictionary):
	"""
	Takes a dictionary as input and creates a list of keys and a list of values.
	Returns two lists as a list.
	"""
	key_list = []
	value_list = []

	for key in dictionary:
		key_list.append(key)
		value_list.append(dictionary[key])

	return [key_list, value_list]

def normalize_dist(unnormalized_dist):
	"""
	normalizes a distribution
	"""
	# print "Normalizing distribution ..."
	normalized_dist = {}
	sum_of_values = 0
	for key in unnormalized_dist:
		sum_of_values += unnormalized_dist[key]
	
	for key in unnormalized_dist:
		normalized_dist[key] = unnormalized_dist[key] / float(sum_of_values)
		if normalized_dist[key] < 0:
			return "normal_dist values less than zero:", normalized_dist[key]
	return normalized_dist

def gen_iter_graph(final_nodes, num_nodes):
	""" 
	generates a random directed graph iteratively, where in each iteration a new node is created and added to the graph, connected to a subset of the existing nodes.  The subset is chosen based on in-degrees of existing nodes. 

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
		trial = DPATrial.DPATrial(num_nodes)
		V_prime = trial.run_trial(num_nodes)
		for node in V_prime:
			V_prime.add(node)
		V.append(node_added)
		graph[node_added] = V_prime
	return graph


# plot results via log/log plot of points in normalized distribution using simpleplot (log x and y axis)
fig, ax =  plt.subplots()



# -------------------------------------------------------------------------
#  Citation graph for all questions
##
# load graph
cit_graph = load_graph(CITATION_URL)
# compute in-degrees
cit_in_deg = compute_in_degrees(cit_graph)


# linear graph of citations
# plot to find average for # 3
# cit_coords = dict_to_coord_lists(cit_in_deg)
# plt.plot(cit_coords[0], cit_coords[1], '.')
# plt.yscale('linear')
# ax.set_xlabel('# times cited (linear)', fontsize=8)
# ax.set_ylabel('# papers citing (linear)', fontsize=8)
# plt.grid(True)
# plt.title('Citations - Linear', fontsize=10)


# To normalize the distribution, sum to one by simply dividing each value by the total number of nodes (NOTE: total # of edges, not nodes).
cit_normal_dist = normalize_dist(cit_in_deg)
# plt.subplot(1,2,2)
cit_coords = dict_to_coord_lists(cit_normal_dist)
plt.loglog(cit_coords[0], cit_coords[1], '.')
ax.set_xlabel('times cited/in-degrees (log-scale)', fontsize=8)
ax.set_ylabel('fraction of papers citing/ (log-scale, normalized)', fontsize=8)
plt.grid(True)
plt.title('Citations in-degree distribution', fontsize=10)



# ------------------------------------------------------------------------
# Question 1 and 2
##
# load graph
# q2_graph = gen_random_graph(5000, .8)
# # compute in-degrees
# q2_in_deg = compute_in_degrees(q2_graph)
# # normalize distribution
# q2_normal_dist = normalize_dist(q2_in_deg)
# # plot results
# # plt.subplot(2,2,3)
# q2_coords = dict_to_coord_lists(q2_normal_dist)
# plt.loglog(q2_coords[0], q2_coords[1],'.')
# ax.set_xlabel('in-degrees', fontsize=9)
# ax.set_ylabel('nodes', fontsize=9)
# plt.grid(True)
# plt.title('In-degree distribution of ER algorithm', fontsize=10)



# ------------------------------------------------------------------------
# Question 2 algorithm test
##
# print "make_complete_graph(3):"
# print make_complete_graph(3)
# gen_random_graph(3, .8)
# ------------------------------------------------------------------------



# ------------------------------------------------------------------------
# Question 3 and 4 graph
##
# Question 3
# final_nodes = 27000
# # num_nodes should be close to the average out-degree of the physics citation graph
# num_nodes = 250

# # # Question 4 
# # # load graph
# q4_graph = gen_iter_graph(final_nodes, num_nodes)
# # compute in-degrees
# q4_in_deg = compute_in_degrees(q4_graph)
# # normalize distribution
# q4_normal_dist = normalize_dist(q4_in_deg)
# # plot results
# # plt.subplot(1,2,1)
# coords = dict_to_coord_lists(q4_normal_dist)

# # NOTE:  tis was likely the error in first homework submission !!!!!
# # take log of coords
# x_val = [math.log1p(coords[0]) for coords[0] in coords]
# y_val = [math.log1p(float(coords[1]) / len(q4_graph))]

# plt.loglog(coords[0], coords[1],'.')
# ax.set_xlabel('in-degrees (log-scale)', fontsize=10)
# ax.set_ylabel('nodes (log-scale, normalized)', fontsize=10)
# plt.grid(True)
# plt.title('In-degree distribution: Iterative-random Graph', fontsize=10)
# -------------------------------------------------------------------------


# formatting
# plt.subplots_adjust(top=0.95, bottom=0.08, left=0.10, right=0.95, hspace=0.25, wspace=0.35)
plt.draw()
plt.show()