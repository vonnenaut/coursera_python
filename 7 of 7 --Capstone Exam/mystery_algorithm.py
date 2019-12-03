# Fundamentals of Computing Capstone Exam
# Questions 21 - 25
# Mystery algorithm
from itertools import combinations

EX_GRAPH0 = {1: set([2]),
             2: set([1]),
             3: set([])
            }

EX_GRAPH1 = {1: set([]),
             2: set([3])}


Q21_GRAPH = {1: set([2,3,4,5,6,7]),
             2: set([1,3,7]),
             3: set([1,2,4]),
             4: set([1,3,5]),
             5: set([1,4,6]),
             6: set([1,5,7]),
             7: set([1,2,6])
}

"""
Example graphs for Question 25 on the Capstone Exam
"""

# Example graphs

GRAPH1 = {1 : set([]), 2 : set([3, 7]), 3 : set([2, 4]), 4 : set([3, 5]), 5 : set([4, 6]), 6 : set([5, 7]), 7 : set([2, 6])}

GRAPH2 = {1 : set([2, 3, 4, 5, 6, 7]), 2 : set([1]), 3 : set([1]), 4 : set([1]), 5 : set([1]), 6 : set([1]), 7 : set([1])}

GRAPH3 = {0: set([4, 7, 10]), 1: set([5, 6]), 2: set([7, 11]), 3: set([10]), 4: set([0, 7, 11]), 5: set([1, 7]), 6: set([1]), 7: set([0, 2, 4, 5, 9, 11]), 8: set([9]), 9: set([7, 8]), 10: set([0, 3]), 11: set([2, 4, 7])}

GRAPH4 = {0: set([4, 7, 10, 12, 13]), 1: set([5, 6, 12]), 2: set([7, 11, 12, 14]), 3: set([10, 14, 15]), 4: set([0, 7, 11, 12, 13, 14]), 5: set([1, 7, 15]), 6: set([1, 13]), 7: set([0, 2, 4, 5, 9, 11, 14]), 8: set([9, 14, 15]), 9: set([7, 8]), 10: set([0, 3]), 11: set([2, 4, 7]), 12: set([0, 1, 2, 4]), 13: set([0, 4, 6, 15]), 14: set([2, 3, 4, 7, 8]), 15: set([3, 5, 8, 13])}

GRAPH5 = {0: set([4, 7, 10, 12, 13, 16]), 1: set([5, 6, 12]), 2: set([7, 11, 12, 14]), 3: set([10, 14, 15]), 4: set([0, 7, 11, 12, 13, 14, 17]), 5: set([1, 7, 15]), 6: set([1, 13]), 7: set([0, 2, 4, 5, 9, 11, 14, 18]), 8: set([9, 14, 15]), 9: set([7, 8, 19]), 10: set([0, 3]), 11: set([2, 4, 7]), 12: set([0, 1, 2, 4]), 13: set([0, 4, 6, 15, 16]), 14: set([2, 3, 4, 7, 8]), 15: set([3, 5, 8, 13]), 16: set([0, 13, 19]), 17: set([4]), 18: set([7]), 19: set([9, 16])}

GRAPH6 = {0: set([4, 7, 10, 12, 13, 16]), 1: set([5, 6, 12]), 2: set([7, 11, 12, 14]), 3: set([10, 14, 15]), 4: set([0, 7, 11, 12, 13, 14, 17]), 5: set([1, 7, 15]), 6: set([1, 13]), 7: set([0, 2, 4, 5, 9, 11, 14, 18]), 8: set([9, 14, 15]), 9: set([7, 8, 19]), 10: set([0, 3]), 11: set([2, 4, 7]), 12: set([0, 1, 2, 4]), 13: set([0, 4, 6, 15, 16]), 14: set([2, 3, 4, 7, 8]), 15: set([3, 5, 8, 13]), 16: set([0, 13, 17, 19]), 17: set([4, 16]), 18: set([7]), 19: set([9, 16])}


def mystery(graph):
    """ V:    set of vertices/nodes
        E:    set of edges
        Input:  Undirected graph g = (V, E)
        Output:  Subset V' C underline V that satisfies some property. """
    # n <-- |V|
    num_nodes = len(graph)

    # for i <- 0 to n do
    for subset_size in range(1,2):
        print "\n\n\n------------------------------------"
        print "subset_size:", subset_size
        # foreach subset V' of V of size i do, i.e., for each subset of nodes
        for subset in set(combinations(graph,subset_size)):
            print "\n\n\n\n\n///// subset:", subset, "/////"
            flag = True
            # foreach e Element of E do, i.e., for each edge in the graph
            for node, edges in graph.iteritems():
                print "\nnode:%r" % node
                # if e in intersection with V' = null then, i.e., if the edge is not in the subset's group of edges
                print "subset:", subset
                print "set(subset):", set(subset)
                print "edges:", edges
                if not set(subset).intersection(edges):
                     flag = False
            print "\nflag:", flag
            if flag:
                return subset


# Testing
print "\n\n---------------------------"
print "Testing ..."
# print "\n\n--------------------------"
# print "EX_GRAPH0"
# input = EX_GRAPH0
# print "\n\nmystery algorithm input:\n %r \n\nmystery algorithm output:\n %r " % (input, mystery(input))


# print "mystery(GRAPH1):", mystery(GRAPH1)
print len(mystery(GRAPH1))     # answer should be 3
# print len(mystery(GRAPH2))     # answer should be 1
# print len(mystery(GRAPH3))     # answer should be 6
# print len(mystery(GRAPH4))     # answer should be 9
# print len(mystery(GRAPH5))
# print len(mystery(GRAPH6))
# print "-------------------------------"

# print "\n\n--------------------------"
# print "EX_GRAPH1"
# input = EX_GRAPH1
# print "\n\nmystery algorithm input:\n %r \n\nmystery algorithm output:\n %r " % (input, mystery(input))

# print "\n\n--------------------------"
# print "Q21_GRAPH"
# input = Q21_GRAPH
# print "\n\nmystery algorithm input:\n %r \n\nmystery algorithm output:\n %r " % (input, mystery_algo(input))