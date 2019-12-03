"""
Algorithmic Thinking 1
week 4
Project #2
Implement breadth-first search and compute connected components (CCs) of an undirected graph as well as the size of its largest CC and finally, compute resilience of a graph, measured by the size of its largest CC as aa sequence of nodes are deleted from the graph.
"""
from collections import deque
import poc_simpletest as simpletest

# globals
RESILIENCE = []

# bfs-visited pseudo-code
# Input:  Undirected graph g = (V, E); source node i.
# Output:  Visited; the set of all nodes visited by the algorithm
# Initialize Q to an empty queue;
# Visited <-- {i};
# enqueue(Q, i);
# while Q is not empty do
# 	j <-- dequeue(Q);
# 	foreach neighbor h of j do
# 		if h not an element of Visited then
# 			Visited <-- Visited U {h};
# 			enqueue(Q,h);

# return Visited;

def bfs_visited(ugraph, start_node):
	""" takes undirected graph and node as input;
	returns set of all nodes visited by breadth-first search starting at start_node """
	queue = deque()
	visited = set([start_node])

	queue.append(start_node)
	print "start_node:", start_node

	while len(queue) > 0:
		current_node = queue.pop()
		print "current_node:", current_node
		for neighbor in ugraph[current_node]:
			if neighbor not in visited:
				visited.add(neighbor)
				queue.append(neighbor)
	return visited


def bfs_visited_test():
	""" tests bfs_visted """
	graph = {0: {1, 2},
		 	 1: {0},
		 	 2: {0, 4, 7},
		 	 4: {2},
		 	 5: {6},
		 	 6: {5},
		 	 7: {2, 8},
		 	 8: {7}}
	node = 0
	return bfs_visited(graph, node)


# cc_visited pseudocode
# Input:  Undirected graph g = (V, E).
# Output: CC:  the set of connecte components of graph g.

# RemainingNodes <-- V;
# CC <-- Null;

# while RemainingNodes != Null do
# 	Let i be an arbitrary node in RemainingNodes;
# 	W <-- BFS-Visited(g,i);
# 	CC <-- CC union {W};
#   RemainingNodes <--RemainingNodes - W;
# return CC;


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
		[remaining_nodes.remove(ws_item) for ws_item in working_set if ws_item in remaining_nodes]
	return c_comp


def cc_visited_test():
	""" tests cc_visted """
	graph = {0: {1, 2},
		 1: {0},
		 2: {0},
		 3: {},
		 4: {5, 6},
		 5: {4, 6},
		 6: {4, 5},
		 7: {8},
		 8: {7}}

	return cc_visited(graph)


def largest_cc_size(ugraph):
	""" computes and returns the size of the largest connected component of ugraph; returns an int """
	largest_num = 0
	largest_set = None

	c_comp = cc_visited(ugraph)

	for group in c_comp:
		if len(group) > largest_num:
			largest_num = len(group)
			largest_set = group
	return largest_num


def largest_cc_size_test():
	""" tests largest_cc_size """
	graphs = [
		{0: {1, 2},
	 	 1: {0},
		 2: {0},
		 3: {},
		 4: {5, 6},
		 5: {4, 6},
		 6: {4, 5},
		 7: {8},
		 8: {7}
		 },
		{0: {1},
		 1: {2, 3, 4, 5},
		 2: {1, 3, 4, 5},
		 3: {1, 2, 4, 5},
		 4: {1, 2, 3, 5},
		 5: {1, 2, 3, 4}
		 },
		{0: {},
		 1: {2, 3, 4, 5},
		 2: {1, 3, 4, 5},
		 3: {1, 2, 4, 5},
		 4: {1, 2, 3, 5},
		 5: {1, 2, 3, 4}
		 },
		{0: {},
		 1: {2},
		 2: {1},
		 3: {},
		 4: {5},
		 5: {4}
		 }
		]

	results = []

	for graph in graphs:
		results.append(largest_cc_size(graph))

	return results


def compute_resilience(ugraph, attack_order):
	""" takes an undirected graph and a list of nodes, attack_order;
	iterates through the nodes in attack_order.
	For each node, removes the given node and its edges from ugraph and then computes the size of the largest cc for the resulting graph.  
	returns a list whose k + 1th entry is the size of the largest cc in the graph after removal of the first k nodes in attack_order.  The first entry in the returned list is the size of the largest cc in the original graph"""
	resilience = []
	resilience.append(largest_cc_size(ugraph))
	# iterate through nodes in attack_order
	for target in attack_order:
		print "\ntarget:", target
		# in order to remove given node and its edges from ugraph
		# first create a list of neighbor nodes to visit for removal of edges
		neighbors = bfs_visited(ugraph, target)
		# then visit each neighbor, removing target from its list of neighbors
		for neighbor in neighbors:
			if target in ugraph[neighbor]:
				ugraph[neighbor].remove(target)
		# next remove the target node
		del ugraph[target]
		# compute size of largest cc for resulting graph
		largest_cc = largest_cc_size(ugraph)
		# append largest cc to result list
		resilience.append(largest_cc)

	# return result list
	print "\nresilience:", resilience
	return resilience


def compute_resilience_test():
	""" tests compute_resilience """
	graphs = [
		{0: {1, 2},
	 	 1: {0},
		 2: {0},
		 3: {},
		 4: {5},
		 5: {4},
		 6: {},
		 7: {8},
		 8: {7}
		 },
		{0: {},
		 1: {2},
		 2: {1, 3, 4},
		 3: {2, 5},
		 4: {2},
		 5: {3}
		 },
		{0: {},
		 1: {2, 3},
		 2: {1, 3, 4},
		 3: {1, 2, 4},
		 4: {2, 3},
		 5: {6},
		 6: {5}
		 },
		{0: {},
		 1: {2, 3},
		 2: {1},
		 3: {1, 4},
		 4: {3, 5},
		 5: {4}
		 }
		]

	attack_orders = [
		[0, 5],
		[2, 3],
		[2, 3, 1],
		[0, 3]
	]

	results = []

	counter = 1
	for graph in graphs:
		print "\n\nTest %d begin ..." % counter
		print "\ngraph:\n", graph
		attack_o = attack_orders[graphs.index(graph)]
		print "\nattack_order:", attack_o		
		results.append(compute_resilience(graph, attack_o))
		print "\n///// test %d complete /////\n\n" % (counter)
		counter += 1

	return results


# Tests
def run_tests():
	"""Testing apparatus for all functions in project2 """
	test = simpletest.TestSuite()
	print "\n\nRunning tests ..."
	test.run_test(bfs_visited_test(), set([0, 1, 2, 4, 7, 8]), "\n///// bfs_visited_test failed: /////\n")
	test.run_test(cc_visited_test(), [set([8, 7]), set([4, 5, 6]), set([3]), set([0, 1, 2])], "\n///// cc_visited_test failed: /////\n")
	test.run_test(largest_cc_size_test(), [3, 6, 5, 2], "\n///// largest_cc_size_test failed: /////\n")
	test.run_test(compute_resilience_test(), [[3, 2, 2], [5, 2, 1], [4, 3, 2, 2], [5, 5, 2]], "\n///// compute_resilience_test failed: ///// \n")

	print "\n\n------------------------"
	test.report_results()

run_tests()

