def compute_resilience(ugraph, attack_order):
	""" takes an undirected graph and a list of nodes, attack_order;
	iterates through the nodes in attack_order.
	For each node, removes the given node and its edges from ugraph and then computes the size of the largest cc for the resulting graph.  
	returns a list whose k + 1th entry is the size of the largest cc in the graph after removal of the first k nodes in attack_order.  The first entry in the returned list is the size of the largest cc in the original graph"""
	global RESILIENCE
	comp_to_prune = None

	if attack_order == []:
		RESILIENCE.append(largest_cc_size(ug_copy))
		print "final resilience:", RESILIENCE
		return RESILIENCE

	# assign first attack node and append current graph's largest cc to resilience list
	node = attack_order.pop()
	RESILIENCE.append(largest_cc_size(ugraph))
	print "RESILIENCE:", RESILIENCE

	# isolate cc relating to current attack node for pruning
	ccs = cc_visited(ugraph)
	for component in ccs:
		if node in component:
			comp_to_prune = component

	# prune cc 
	if comp_to_prune == None:
		return
	for component in comp_to_prune:
		for value in comp_to_prune:
			if value in :
				ugraph[component].remove(value)			
	
	# delete the attack node
	del ugraph[node]

	# recursively call function again
	return compute_resilience(ugraph, attack_order)