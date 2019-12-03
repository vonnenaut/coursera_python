""" 
Algorithmic Thinking 2
Week 2 Project (#3)
Implement and Assess 2 Methods for Clustering Data
and implementing 
2 methods for computing closest pairs
and 
2 methods for clustering data

Student will implement five functions:
slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)
where cluster_list is a 2D list of clusters in the plane


IMPORTANT NOTE:
As one important coding note, you may need to sort a list of clusters by the vertical (or horizontal) positions of the cluster centers. A sort by vertical position can be done in a single line of Python using the sort method for lists by providing a key argument of the form:
		cluster_list.sort(key = lambda cluster: cluster.vert_center())
"""
import math, random
import alg_cluster
# import alg_clusters_matplotlib as plot


######################################################
# Code for closest pairs of clusters


def sort_vert(cluster_list, x_indices):
	""" sorts a cluster_list by the vertical positions of the cluster centers """
	x_values = []

	# print "\n\nsort_vert:  cluster_list:", cluster_list
	cluster_list_sorted = cluster_list.sort(key = lambda cluster: cluster.vert_center())
	# print "\ncluster_list_sorted:", cluster_list_sorted
	for cluster in cluster_list_sorted:
		x_values.append(cluster.horiz_center())
	return x_values


def distance(cluster1, cluster2):
    """
    Compute the Euclidean distance between two clusters
    """
    # print "cluster1:", cluster1
    vert_dist = cluster1.vert_center() - cluster2.vert_center()
    horiz_dist = cluster1.horiz_center() - cluster2.horiz_center()
    return math.sqrt(vert_dist ** 2 + horiz_dist ** 2)


def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    # print "\n///////////// pair_distance /////////////"
    # print "indices: [%r, %r] \t x values: [%r, %r]" % (idx1, idx2, cluster_list[idx1].horiz_center(), cluster_list[idx2].horiz_center())
    # print cluster_list[idx1].distance(cluster_list[idx2])
    # print "/////////////////  ///////////////////\n"
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    A brute-force closest pair method which finds the closest pair of clusters in a cluster list.  cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.

    Input:  list of cluster objects
	Output:  returns a closest pair tuple (dist, idx1, idx2) where idx1 < idx2

	Algorithm 3:  SlowClosestPair
	Input:  A set P of (>=2) points whose ith point, pi, is a pair (xi, yi).
	Output:  A tuple (d,i,j) where d is the smallest pairwise distance of points in P and i,j are the indices of two points whose distance is d.

	(d,i,j) <-- (infinity, -1, -1);
	foreach pu Element of P do
		foreach pv Element of P (u != v) do
			(d,i,j) <-- min{(d,i,j), (d sub(pu,pv),u,v)};  // min compares the first element of each tuple

	return(d,i,j);     
    """
    output_list = [99999, -1, -1]
    # print "\ncluster_list:", cluster_list, "\n"

    for index1 in range(len(cluster_list)):
    	for index2 in range(1,len(cluster_list)):
    		temp_dist = pair_distance(cluster_list, index1, index2)
    		if output_list[0] > temp_dist[0] and index1 != index2:
    			output_list = [temp_dist[0], temp_dist[1], temp_dist[2]] 	
    return tuple(output_list)


def fast_closest_pair(cluster_list):
    """
    A divide-and-conquor closest pair method which computes the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.   


	https://www.coursera.org/learn/algorithmic-thinking-2/discussions/all/threads/qZyCitkxEeaWQQ6gG0GoTg

	Given each of these points:
	0: alg_cluster.Cluster(set([]), 1.0, 0.0, 1, 0)
	1: alg_cluster.Cluster(set([]), 4.0, 0.0, 1, 0)
	2: alg_cluster.Cluster(set([]), 5.0, 0.0, 1, 0)
	3: alg_cluster.Cluster(set([]), 7.0, 0.0, 1, 0)

	The algorithm given in this class works like:
    #1 split the list into two lists [0,1], [2,3]

	#2.1 call fast_closest_pair([0,1])
	#2.2 this calls slow_closest_pair([0,1]) and (3.0, 0, 1) is returned

	#3.1 call fast_closest_pair([2,3])
	#3.2 this calls slow_closest_pair([2,3]) and (2.0, 0, 1) is returned

	# 4 call closest_pair_strip([0,1,2,3], 4.5, 2.0) and (1.0, 1,2) is returned (4.5 = (4.0+5.0)/2 and 2.0 is shorter value of 2.0 and 3.0 

	# 5 returned 1.0 is smaller than 2.0, the value from the strip is the closest pair.
    """
    # sort in nondecreasing order of horizontal (x) coordinates
    cluster_list.sort(key=lambda cluster: cluster.horiz_center())

    # n <-- length(P);
    len_cluster = len(cluster_list)

	# if n <= 3 then
    if len_cluster <= 3:
    	# (d,i,j) <== SlowClosestPair(P);
    	output_list = slow_closest_pair(cluster_list)
    	# print "\n\n\n\n//////////// START slow_cp ////////////\n"
    	# print "slow_closest_pair cluster_list:\n", cluster_list
    	# print "OUTPUT:", output_list
    	# print "\n\n//////////// END slow_cp ////////////\n\n\n\n"
    else:
    	# m <-- leftbracketwithouttop n/2 rightbracketwithouttop
    	middle_index = int(math.floor(len_cluster/2))
    	# Psub L <-- {pi: 0 <= i <= m-1}; Pr <--{pi: m <= i <= n-1};  // Psub L and Pr are also sorted
    	# (dL, iL, jL) <-- FastClosestPair(PL);
		# (dr, ir, jr) <-- FastClosestPair(Pr);

    	left_output_list = fast_closest_pair(cluster_list[0:middle_index])
    	right_output_list = fast_closest_pair(cluster_list[middle_index: len_cluster])
    	
    	# print "\n\nsorted cluster_list:", cluster_list
    	# print "\n\nleft_output_list:", left_output_list
    	# print "right_output_list:", right_output_list
    	# print "middle_index:", middle_index

    	output_list = min(left_output_list, (right_output_list[0], right_output_list[1]+middle_index, right_output_list[2]+middle_index))
    	# TODO:  mid and half-width may be getting calculated incorrectly for Test #16.
    	# print "cluster_list[middle_index-1].horiz_center():", cluster_list[middle_index-1].horiz_center()
    	# print "cluster_list[middle_index].horiz_center():", cluster_list[middle_index].horiz_center()
    	mid = 1/2.0*(cluster_list[middle_index-1].horiz_center()+cluster_list[middle_index].horiz_center())
    	# print "cluster_list[-1].horiz_center():", cluster_list[-1].horiz_center()
    	# print "cluster_list[0].horiz_center():", cluster_list[0].horiz_center()
    	half_width = abs(cluster_list[-1].horiz_center()-cluster_list[0].horiz_center())

    	# print"\n\n\n\npassing mid = %r and half_width = %r to cp_strip ..." % (mid, half_width)
    	# print "\n\n/////////////// START cp_strip ////////////////\n"
    	# print "closest_pair_strip(cluster_list, mid, half_width):", closest_pair_strip(cluster_list, mid, half_width)
    	# print "output_list:", output_list
    	output_list = min(output_list, closest_pair_strip(cluster_list, mid, half_width))
    	# print "\n\n///////////// END cp_strip //////////////\n\n\n\n"
    return output_list


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.  

    	Algorithm 5:  ClosestPairStrip
		Input:  A set P of points whose ith point, pi, is a pair (xi, yi); mid and w, both of which are 	real numbers.
		Output:  A tuple (d,i,j) where d is the smallest pairwise distane of points in P whose 	horizontal (x) coordinates are within w from mid.
	
		Let S be a list of the set {i: length(xi - mid) < w};
		Sort the indices in S in nondecreasing order of the vertial (y) coordinates of their associated points;
		k <-- length(S);
		(d,i,j) <-- (infinity, -1, -1);
		for u <-- 0 to k - 2 do
			for v <-- u + 1 to min{u+3,k-1} do
				(d,i,j) <-- min{(d,i,j),(dsub(pS[u],PS[v]), S[u],S[v])}
		return(d,i,j)     
    """
    cl_copy = cluster_list[:]
    indices = []   

    # Let S be a list of the set {i: |xi - mid| < half_width}
    # print "\ncp_strip horiz_center:", horiz_center
    indices = [index for index in range(len(cl_copy)) if abs(cl_copy[index].horiz_center()-horiz_center)<=half_width]
    
    # FOR TESTING PURPOSES ##############################################
    # print "\n\n////////\nindices: \t%r \n////////\n\n\n" % indices

    # print "Clusters:\n-------"
    # for cluster in cl_copy:
    # 	print cluster
    
   #  print "\n\n--------------------- Distances --------------------- "
   #  for index1 in range(len(cluster_list)):
   #      for index2 in range(1, len(cluster_list)):
			# if index1 != index2:
			# 	print "*****"
			# 	print "\n\nclusters: [%r, %r]  distance: %r" % (index1, index2, cluster_list[index1].distance(cluster_list[index2]))
			# 	print "cluster %r: %r" % (index1, cluster_list[index1])
			# 	print "cluster %r: %r \n\n" % (index2, cluster_list[index2])
   #  print "----------------------- ----------------------- \n\n"
	# END TESTING CODE -----------------------
	
	# Sort the indices in S in nondecreasing order of the vertial (y) coordinates of their associated points;
    cl_copy_sorted = cl_copy[:]
    cl_copy_sorted.sort(key = lambda cluster: cluster.vert_center())
    # print "\n\nClusters (sorted vertically):\n-------"
    # for cluster in cl_copy_sorted:
    # 	print cluster

    # k <-- length(S);
    len_indices = len(indices)

    # (d,i,j) <-- (infinity, -1, -1);
    output_list = [float('inf'), -1, -1]	

    # for u <-- 0 to k - 2 do
    for value1 in range(len_indices-1):
    	# 	for v <-- u + 1 to min{u+3,k-1} do
        for value2 in range(value1+1, min(value1+6,len_indices)):
            # print "\n\n ////value1/2: [%r %r]" % (value1, value2)
            # (d,i,j) <-- min{(d,i,j),(dsub(psubS[u],PsubS[v]), S[u],S[v])}
            min_dist = min(output_list[0], pair_distance(cl_copy,indices[value1],indices[value2])[0])
            # print "min_dist:", min_dist
            if output_list[0] > min_dist:
            	# print "indices[value1]:", indices[value1]
            	# print "indices[value2]:", indices[value2]
            	output_list = [pair_distance(cl_copy,indices[value1],indices[value2])[0], indices[value1], indices[value2]]

	# For Testing purposes ##################################################################
	# print "\n\n\n############################\n\tResults\n############################\n"
	# # print "\ncluster_list:", cluster_list
 #    print "\nhoriz_center:", horiz_center
 #    print "half_width:", half_width, "\n"
 #    print "indices:", indices
 #    print "output_list:", output_list, "\n"
 #    # print "cl_copy:", cl_copy, "\n\n"
 #    print "cluster 1: % r  \ncluster 2: %r" % (cl_copy[output_list[1]], cl_copy[output_list[2]])
    ########################################################################################

    # For Testing purposes -- graph clusters
    # plot.plot_clusters()

    # return(d,i,j)
    # print "cps_output_list:", output_list
    return tuple(output_list)
            
 
    
######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
 
    Algorithm 1: Hierarchical Clustering
	Input:  A set P of points wose ith point, pi is a pair (xi, yi); k, the desired number of clusters.
	Output:  A set C of k clusters that provides a clustering of the points in P.

	NOTE:  Lines 5 and 6 need not be implemented verbatim.  In particular, merging one cluster into the other using merge_clusters and then removing the other cluster is fine.  For this function, mutating cluster_list is allowed to improve performance.
    """
    # print "\n\ncluster_list:\n", cluster_list, "\n\n"
    # n <-- |P|
    len_cluster_list = len(cluster_list)
	
	# Initialize n clusters C = {C1, ... Cn} such that Ci = {pi};
    new_cluster_list = []

    for index in range(len_cluster_list):
		new_cluster_list.append(alg_cluster.Cluster(cluster_list[index].fips_codes(), cluster_list[index].horiz_center(), cluster_list[index].vert_center(), cluster_list[index].total_population(), cluster_list[index].averaged_risk()))

    # while |C| > k do
    while len(new_cluster_list) > num_clusters:
    	# (Ci,Cj) <-- argminCi,Cj Element C, i != j^dCi,Cj;
    	# C <-- C Union {Ci Union Cj};  // line 5
		# C <-- C \ {Ci, Cj};			  // line 6
    	fc_pair = fast_closest_pair(new_cluster_list)
    	# print "\nfc_pair:", fc_pair, "\n"
    	new_cluster_list[fc_pair[1]].merge_clusters(new_cluster_list[fc_pair[2]])
    	del new_cluster_list[fc_pair[2]]
    	# new_cluster_list.append(cluster_list[fc_pair[1]])
    	# del cluster_list[fc_pair[1]]

    # print "k = %r \n\nnew_cluster_list: \n%r" % (num_clusters, new_cluster_list)
    return new_cluster_list


######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list

	Input:  A set P of points whose ith point, pi, is a pair (xi, yi); k, the desired number of clusters, q, a number of iterations.
	Output:   A set C of k clusters that provides a clustering fo the points in P.

    (OWLTest Error: Disallowed Input Parameter Mutation)
    """
    # print "\n\ncluster_list:", cluster_list
    print "\n\nnum_clusters:", num_clusters
    print "num_iterations:", num_iterations, "\n"
    new_cluster_groups = []
    cl_copy = cluster_list[:]

    # n <-- |p|;
    len_cluster_list = len(cluster_list)

    # Initialize old cluster using large population counties; Initialize k (num_clusters) centers mu1, ..., muk to initial values (each mu is a point in 2D space);      
    # position initial clusters at the location of clusters with largest populations (i.e., greatest # of FIPS codes) 
    # NOTE:  Cluster centers computed in lines 2 and 8-9 should stay fixed as lines 5-7 are executed during one iteration of the outer loop.  To avoid modifying these values during execution of lines 5-7,  you should consider storing these cluster centers in a separate data structure.
    cluster_centers = []
    temp_cl = cl_copy[:]
    
    temp_cl.sort(key=lambda cluster: len(cluster.fips_codes()))
    for cluster in reversed(temp_cl):
    	if len(cluster_centers) < num_clusters:
			cluster_centers.append([cluster.horiz_center(), cluster.vert_center()])
	
	# print "cluster_centers:", cluster_centers

	# for i <-- 1 to q do
	# For number of iterations
    for dummy_var in range(num_iterations):
	    # initialize k (num_clusters) empty sets C1, ... Ck;
	    # NOTE:  represent an empty cluster as a Cluster object whose set of counties is empty and whose total population is zero
	    # Initialize the new clusters to be empty 
        for index in range(num_clusters):
        	new_cluster_groups.append(alg_cluster.Cluster(set(), cluster_centers[index][0], cluster_centers[index][1], 0, 0))
        # print "new_cluster_groups:", new_cluster_groups

	    # for j = 0 to n - 1 do
	    # For each county
        for dummy_var in range(0, len_cluster_list-1):
	        # L <-- argminsub(1<=f<=k) (dsub(psubj), musubf);
	        # Find the old cluster center that is closest 
	        #  NOTE:  Should below be old cluster?
	        closest_pair = fast_closest_pair(cl_copy)
	        # C sub L <-- C sub L Union {psub j};  // handled with Cluster class merge_clusters method, which will automatically update the cluster centers to correct locations.
	        # Add the county to the corresponding new cluster 
	        new_cluster_groups.append(cl_copy[closest_pair[1]].merge_clusters(cl_copy[closest_pair[2]]))
	    # Set old clusters equal to new clusters 

	    # for f = 1 to k do
        print "\n\n"
        for value in range(num_clusters):
	        # muf = center (Cf)     // handled with Cluster class built-in method(s)
	        # print "\n\n[new_cluster_groups[value].horiz_center(), new_cluster_groups[value].vert_center()]:", [new_cluster_groups[value].horiz_center(), new_cluster_groups[value].vert_center()]
	        cluster_centers[value] = [new_cluster_groups[value].horiz_center(), new_cluster_groups[value].vert_center()]

    # return {C1, C2, ..., Ck};
    # Return the new clusters       
    return new_cluster_groups


