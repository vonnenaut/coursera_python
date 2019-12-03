def compute_resilience(ugraph, attack_order):
	""" takes an undirected graph and a list of nodes, attack_order;
	iterates through the nodes in attack_order.
	For each node, removes the given node and its edges from ugraph and then computes the size of the largest cc for the resulting graph.  
	returns a list whose k + 1th entry is the size of the largest cc in the graph after removal of the first k nodes in attack_order.  The first entry in the returned list is the size of the largest cc in the original graph"""
	ug_copy = deepcopy(ugraph)
	resilience = []

	if attack_order == []:
		resilience.append(largest_cc_size(ug_copy))
		print "final resilience:", resilience
		return resilience

	node = attack_order.pop()
	resilience.append(largest_cc_size(ug_copy))

	if node in ug_copy:			
		temp_ug_copy = deepcopy(ug_copy)
		for key in ug_copy:
			for value in ug_copy[key]:
				if value == node:
					temp_ug_copy[key].remove(value)
		ug_copy = temp_ug_copy.copy()
	del ug_copy[node]
	return compute_resilience(ug_copy, attack_order)