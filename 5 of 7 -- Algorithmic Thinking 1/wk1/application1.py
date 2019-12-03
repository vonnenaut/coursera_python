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
	else:
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

# load graph
citation_graph = load_graph(CITATION_URL)
# compute in-degrees
in_deg = compute_in_degrees(citation_graph)
# To normalize the distribution, sum to one by simply dividing each value by the total number of nodes (NOTE: total # of edges, not nodes).
normal_dist = {}
print "Normalizing distribution ..."
normal_dist = {}
sum_of_values = 0
for key in in_deg:
	sum_of_values += in_deg[key]

for key in in_deg:
	normal_dist[key] = in_deg[key] / float(sum_of_values)
	if normal_dist[key] < 0:
		print "normal_dist values less than zero:", normal_dist[key]

# plot results via log/log plot of points in normalized distribution using simpleplot (log x and y axis)
key_list = []
value_list = []
for key in normal_dist:
	key_list.append(key)
	value_list.append(normal_dist[key])

fig, ax =  plt.subplots()
plt.loglog(key_list, value_list, '.')
ax.set_xlabel('number of times cited (log-scale)')
ax.set_ylabel('number of papers citing (log-scale, normalized)')

# plt.subplot(223)
plt.grid(True)
plt.title('High-energy Physics Theory Paper Citations')

plt.draw()
plt.show()

