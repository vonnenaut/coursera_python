"""
Project #1 Description

For your first project, you will write Python code that creates dictionaries corresponding to some simple examples of graphs. You will also implement two short functions that compute information about the distribution of the in-degrees for nodes in these graphs. You will then use these functions in the Application component of Module 1 where you will analyze the degree distribution of a citation graph for a collection of physics papers. This final portion of module will be peer assessed.

Note that this portion of the module should be simple for experienced Python programmers. If you find it challenging, your Python skills may not be sufficient to be successful in this class.

Representing directed graphs

To gain a more tangible feel for how directed graphs are represented as dictionaries in Python, you will create three specific graphs (defined as constants) and implement a function that returns dictionaries corresponding to a simple type of directed graphs. If you are unclear on how to represent a directed graph as a dictionary, we suggest that you review the class notes on graph basics. For this part of the project, you should implement the following:

EX_GRAPH0, EX_GRAPH1, EX_GRAPH2 - Define three constants whose values are dictionaries corresponding to the three directed graphs shown in these linked diagrams: EX_GRAPH0, EX_GRAPH1, and EX_GRAPH2. Note that the label for each node in the diagrams should be represented as an integer. You should use these graphs in testing your functions that compute degree distributions.

Computing degree distributions

For the second part of this project, you will implement two functions that compute the distribution of the in-degrees of the nodes of a directed graph.
"""
import poc_simpletest


EX_GRAPH0 = {0: set([1, 2]),
			 1: set([]),
			 2: set([])}

EX_GRAPH1 = {0: set([1, 5, 4]),
			 1: set([6, 2]),
			 2: set([3]),
			 3: set([0]),
			 4: set([1]),
			 5: set([2]),
			 6: set([])}

EX_GRAPH2 = {0: set([1, 5, 4]), 
			 1: set([2, 6]),
			 2: set([3, 7]), 
			 3: set([7]),
			 4: set([1]),
			 5: set([2]),
			 6: set([]),
			 7: set([3]),
			 8: set([1, 2]),
			 9: set([0, 4, 5, 6, 7, 3])}

GRAPH0 = {0: set([1]),
          1: set([2]),
          2: set([3]),
          3: set([0])}

GRAPH1 = {0: set([]),
          1: set([0]),
          2: set([0]),
          3: set([0]),
          4: set([0])}

GRAPH2 = {0: set([1, 2, 3, 4]),
          1: set([]),
          2: set([]),
          3: set([]),
          4: set([])}

GRAPH3 = {0: set([1, 2, 3, 4]),
          1: set([0, 2, 3, 4]),
          2: set([0, 1, 3, 4]),
          3: set([0, 1, 2, 4]),
          4: set([0, 1, 2, 3])}

GRAPH4 = {"dog": set(["cat"]),
          "cat": set(["dog"]),
          "monkey": set(["banana"]),
          "banana": set([])}

GRAPH5 = {1: set([2, 4, 6, 8]),
          2: set([1, 3, 5, 7]),
          3: set([4, 6, 8]),
          4: set([3, 5, 7]),
          5: set([6, 8]),
          6: set([5, 7]),
          7: set([8]),
          8: set([7])}

GRAPH6 = {1: set([2, 5]),
          2: set([1, 7]),
          3: set([4, 6, 9]),
          4: set([6]),
          5: set([2, 7]),
          6: set([4, 9]),
          7: set([1, 5]),
          9: set([3, 4])}

GRAPH7 = {0: set([1, 2, 3, 4]), 
          1: set([0, 2, 3, 4]), 
          2: set([0, 1, 3, 4]), 
          3: set([0, 1, 2, 4]), 
          4: set([0, 1, 2, 3]), 
          5: set([2, 3, 4]), 
          6: set([0, 1, 4]), 
          7: set([0, 1, 2, 3]), 
          8: set([0, 1, 4, 7]), 
          9: set([2, 4]), 
          10: set([1, 2, 4]), 
          11: set([1, 3, 4, 7]), 
          12: set([0, 2, 3]), 
          13: set([0, 2, 4, 10]), 
          14: set([0, 2, 3, 4, 13])}

GRAPH8 = {0: set([1, 2]), 
          1: set([0, 2]), 
          2: set([0, 1]), 
          3: set([0]), 
          4: set([1, 2]), 
          5: set([0, 2]), 
          6: set([1, 2, 4]), 
          7: set([0, 3]), 
          8: set([0, 1]), 
          9: set([0, 7]), 
          10: set([0]), 
          11: set([0, 1, 3]), 
          12: set([0, 4, 7]), 
          13: set([0, 5]), 
          14: set([0, 1, 8]), 
          15: set([0, 1, 3]), 
          16: set([1, 14, 6]), 
          17: set([0, 8]), 
          18: set([0, 1]), 
          19: set([0, 1, 17])}

GRAPH9 = {0: set([1, 2, 3, 4, 5, 6]),
          1: set([0, 2, 3, 4, 5, 6]),
          2: set([0, 1, 3, 4, 5, 6]),
          3: set([0, 1, 2, 4, 5, 6]),
          4: set([0, 1, 2, 3, 5, 6]),
          5: set([0, 1, 2, 3, 4, 6]),
          6: set([0, 1, 2, 3, 4, 5]),
          7: set([1, 3, 4, 6]),
          8: set([0, 3, 4, 5, 6]),
          9: set([0, 5, 6, 7]),
          10: set([1, 2, 4, 9]),
          11: set([1, 2, 4, 6]),
          12: set([0, 2, 4, 6]),
          13: set([1, 2, 4, 5]),
          14: set([0, 1, 4, 6]),
          15: set([1, 4, 5, 6]),
          16: set([0, 1, 2, 4, 6]),
          17: set([0, 1, 2, 4, 5, 6]),
          18: set([2, 4, 5, 6, 13]),
          19: set([1, 2, 3, 5, 6]),
          20: set([0, 1, 2, 4, 5]),
          21: set([1, 2, 4, 5, 15]),
          22: set([0, 9, 4, 5, 13]),
          23: set([0, 1, 2, 3, 5, 20]),
          24: set([0, 1, 2, 3, 4, 5, 6]),
          25: set([0, 1, 2, 4, 5]),
          26: set([1, 2, 4, 5, 10, 22]),
          27: set([1, 2, 3, 5, 6]),
          28: set([0, 1, 3, 5]),
          29: set([2, 26, 4, 5, 6]),
          30: set([0, 2, 4, 6, 7]),
          31: set([20, 4, 21, 6]),
          32: set([1, 2, 4, 20, 28]),
          33: set([0, 4, 5, 6, 8, 22]),
          34: set([0, 2, 4, 5, 15]),
          35: set([1, 2, 5, 6, 9, 28]),
          36: set([24, 2, 3, 4, 6]),
          37: set([0, 1, 2, 4, 6, 10, 29]),
          38: set([0, 24, 11, 5, 6]),
          39: set([0, 1, 22, 6, 17]),
          40: set([0, 1, 2, 3, 5, 15]),
          41: set([11, 2, 3, 5, 6]),
          42: set([16, 1, 2, 5]),
          43: set([0, 1, 2, 4, 22]),
          44: set([32, 3, 6, 24, 27, 29]),
          45: set([1, 2, 4, 5, 16, 18, 37]),
          46: set([1, 5, 6, 7, 8, 12, 14]),
          47: set([8, 20, 2, 4]),
          48: set([0, 16, 2, 5, 14]),
          49: set([2, 21, 18, 6, 15])}


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
	# print "digraph:", digraph

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
	Takes a directed graph digraph (represented as a dictionary) and computes the unnormalized distribution of the in-degrees of the graph. The function should return a dictionary whose keys correspond to in-degrees of nodes in the graph. The value associated with each particular in-degree is the number of nodes with that in-degree. In-degrees with no corresponding nodes in the graph are not included in the dictionary.

	Note that the values in the unnormalized distribution returned by this last function are integers, not fractions. This unnormalized distribution is easier to compute and can later be normalized to sum to one by simply dividing each value by the total number of nodes.
	"""
	dist_in_degree = {}
	zero_in_count = 0
	
	# Returns:
	# { key, i.e., in-degree, number of edges coming into a node: 
	#   value, i.e., int, number of nodes with this value for in-degree }

	# first, create a temporary 2d list, each interior list containing (1) a key or in-degree and (2) a value or number of nodes with this corresponding in-degree
    # for key in digraph:
    # 	print "digraph:\n %d: %r" % (key, digraph[key])
    print "digraph:", digraph

    node_indegs = compute_in_degrees(digraph)
    print "\nnode_indegs:", node_indegs

	# now that we have our temp list of key-value pairs, let's consolidate any with the same key so as to not have duplicates
	for key in node_indegs:
		print "\nkey: %r, value: %r" % (key, node_indegs[key])
		if node_indegs[key] not in dist_in_degree:
			print "if", node_indegs[key], "not in", dist_in_degree
			dist_in_degree[node_indegs[key]] = 1
			print "dist_in_degree:", dist_in_degree
		elif node_indegs[key] in dist_in_degree:
			print "elif"
			dist_in_degree[node_indegs[key]] += 1
			print "dist_in_degree:", dist_in_degree

	# Finally, let's add a count for nodes with zero in-degrees before creating our final dictionary and returning it
	for node in node_indegs:
		if node_indegs[node] == 0:
			zero_in_count += 1
	if zero_in_count > 0:
		dist_in_degree[0] = zero_in_count

	return dist_in_degree


# OwlTest
##
test = poc_simpletest.TestSuite()
print"----------------------------------------------"
print "Testing compute_in_degrees ...\n"
print "Test 1"
test.run_test(compute_in_degrees(EX_GRAPH0), {0: 0, 1: 1, 2: 1}, "Test 1:  compute_in_degrees(EX_GRAPH0)")
print "Test 2"
test.run_test(compute_in_degrees(EX_GRAPH1), {0: 1, 1: 2, 2: 2, 3: 1, 4: 1, 5: 1, 6: 1}, "Test 2:  compute_in_degrees(EX_GRAPH1)")
print "Test 3"
test.run_test(compute_in_degrees(EX_GRAPH2), {0: 1, 1: 3, 2: 3, 3: 3, 4: 2, 5: 2, 6: 2, 7: 3, 8: 0, 9: 0}, "Test 3:  compute_in_degrees(EX_GRAPH2)")

print"\n----------------------------------------------"
print "Testing in_degree_distribution ...\n"
print "Test 4"
test.run_test(in_degree_distribution(EX_GRAPH0), {0: 1, 1: 2}, "Test 4:  in_degree_distribution(EX_GRAPH0)")
print"\n----------------------------------------------"
print "Test 5"
test.run_test(in_degree_distribution(EX_GRAPH1), {1: 5, 2: 2}, "Test 5:  in_degree_distribution(EX_GRAPH1)")
print"\n----------------------------------------------"
print "Test 6"
test.run_test(in_degree_distribution(EX_GRAPH2), {0: 2, 1: 1, 2: 3, 3: 4}, "Test 6:  in_degree_distribution(EX_GRAPH2)")
print"\n----------------------------------------------"
print "Test 7"
test.run_test(in_degree_distribution(GRAPH0), {1: 4}, "Test 7: in_degree_distribution(GRAPH0)")
print"\n----------------------------------------------"
print "Test 8"
test.run_test(in_degree_distribution(GRAPH1), {0: 4, 4: 1}, "Test 8: in_degree_distribution(GRAPH1)")

# To normalize the distribution, sum to one by simply dividing each value by the total number of nodes.
print"\n----------------------------------------------"
print "Test 9"
# compute in-degrees
print "EX_GRAPH2:", EX_GRAPH2
in_deg = compute_in_degrees(EX_GRAPH2)
print "in_deg:", in_deg
print "Normalizing distribution ..."
normal_dist = {}
print "len(EX_GRAPH2):", len(EX_GRAPH2)
sum = 0
for key in in_deg:
	sum += in_deg[key]

for key in in_deg:
	normal_dist[key] = in_deg[key] / float(sum)
print "normal_dist:", normal_dist

sum_to_one = 0
for key in normal_dist:
	sum_to_one += normal_dist[key]

print "sum_to_one:", sum_to_one

# test.run_test(, {0: 4, 4: 1}, "Test 8: in_degree_distribution(GRAPH1)")

test.report_results()

# [-22.5 pts] in_degree_distribution(alg_module1_graphs.GRAPH1) expected {0: 4, 4: 1} but received {0: 4, 4: 4}










