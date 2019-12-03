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
import math, random, time, alg_cluster
import matplotlib.pyplot as plt


######################################################
# Code for closest pairs of clusters

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
    cl_copy = cluster_list[:]
    output_list = [99999, -1, -1]

    for index1 in range(len(cl_copy)):
    	for index2 in range(1,len(cl_copy)):
    		temp_dist = pair_distance(cl_copy, index1, index2)
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
    else:
        # m <-- leftbracketwithouttop n/2 rightbracketwithouttop
        middle_index = int(math.floor(len_cluster/2))
        # Psub L <-- {pi: 0 <= i <= m-1}; Pr <--{pi: m <= i <= n-1};  // Psub L and Pr are also sorted
        # (dL, iL, jL) <-- FastClosestPair(PL);
        # (dr, ir, jr) <-- FastClosestPair(Pr);
        left_output_list = fast_closest_pair(cluster_list[0:middle_index])
        right_output_list = fast_closest_pair(cluster_list[middle_index: len_cluster])
 
        output_list = min(left_output_list, (right_output_list[0], right_output_list[1]+middle_index, right_output_list[2]+middle_index))
        mid = 1/2.0*(cluster_list[middle_index-1].horiz_center()+cluster_list[middle_index].horiz_center())
        half_width = abs(cluster_list[-1].horiz_center()-cluster_list[0].horiz_center())
        output_list = min(output_list, closest_pair_strip(cluster_list, mid, half_width))

    return output_list


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.   
    """
    indices = []   

    # Let S be a list of the set {i: |xi - mid| < half_width}
    indices = [index for index in range(len(cluster_list)) if abs(cluster_list[index].horiz_center()-horiz_center)<=half_width]
 
	# Sort the indices in S in nondecreasing order of the vertial (y) coordinates of their associated points;
    indices.sort(key = lambda index: cluster_list[index].vert_center())

    cl_sorted = cluster_list[:]
    cl_sorted.sort(key = lambda cluster: cluster.vert_center())

    # k <-- length(S);
    len_indices = len(indices)

    # (d,i,j) <-- (infinity, -1, -1);
    output_list = [float('inf'), -1, -1]	

    # for u <-- 0 to k - 2 do
    for value1 in range(len_indices-1):
    	# 	for v <-- u + 1 to min{u+3,k-1} do
        for value2 in range(value1+1, min(value1+6,len_indices)):
            # (d,i,j) <-- min{(d,i,j),(dsub(psubS[u],PsubS[v]), S[u],S[v])}
            min_dist = min(output_list[0], pair_distance(cluster_list,indices[value1],indices[value2])[0])
            if output_list[0] > min_dist:
                indices_sorted = sorted([indices[value1], indices[value2]])
            	output_list = [pair_distance(cluster_list,indices[value1],indices[value2])[0], indices_sorted[0], indices_sorted[1]]

    # return(d,i,j)
    return tuple(output_list)
            
 
    
######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    """
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
        # C <-- C \ {Ci, Cj};             // line 6
        fc_pair = fast_closest_pair(new_cluster_list)
        # print "\nfc_pair:", fc_pair, "\n"
        new_cluster_list[fc_pair[1]].merge_clusters(new_cluster_list[fc_pair[2]])
        del new_cluster_list[fc_pair[2]]

    return new_cluster_list


######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    """
    points = cluster_list[:]
    
    # n <-- |p|;
    len_points_list = len(points)

    # position initial clusters at the location of clusters with largest populations (i.e., cluster[3] which is population) 
    cluster_centers = []
    temp_cl = points[:]
    
    temp_cl.sort(key=lambda cluster: cluster.total_population())
    for cluster in reversed(temp_cl):
        if len(cluster_centers) < num_clusters:
            cluster_centers.append(alg_cluster.Cluster(set([]), cluster.horiz_center(), cluster.vert_center(), 0, 0))

    # For number of iterations
    for dummy_var in range(num_iterations):
        # initialize k (num_clusters) empty sets C1, ... Ck;
        cluster_groupings = []
        for index in range(len(cluster_centers)):
            cluster_groupings.append(alg_cluster.Cluster(set(), 0, 0, 0, 0))
        # # For each county
        # for j = 0 to n - 1 do
        for index in range(len_points_list):
            # Find the old cluster center that is closest 
            # L <-- argminsub(1<=f<=k) (dsub(psubj), musubf);       
            min_dist = float('inf')
            nearest_cluster_index = None

            for idx, cluster in enumerate(cluster_centers):
                if points[index].distance(cluster) < min_dist:
                    min_dist = points[index].distance(cluster)
                    nearest_cluster_index = idx

            # Add the county to the corresponding new cluster
            # Handled with Cluster class merge_clusters method, which will automatically update the cluster centers to correct locations.
            cluster_groupings[nearest_cluster_index].merge_clusters(points[index])
        # Set old clusters equal to new clusters 
        # for f = 1 to k do
        for index in range(len(cluster_centers)):
            # muf = center (Cf)     // handled with Cluster class built-in method(s)
            cluster_centers[index] = cluster_groupings[index].copy()

    # return {C1, C2, ..., Ck};  
    return cluster_groupings


# Application #3
##########################################################

# Question 1 (2 pts)
def gen_random_clusters(num_clusters):
    """ creates a list of clusters where each cluster in this list corresponds to one randomly generated point in the square with corners (+/-1, +/-1). """
    cluster_list = []

    for county_id in range(num_clusters):
        cluster_list.append(alg_cluster.Cluster(set([str(county_id)]), 10.0*random.random(), 10.0*random.random(), random.random(), random.random()))
    return cluster_list


def compute_runtimes(num_clusters):
    """ compute run-times for slow_closest_pair and fast_closest_pair """
    cluster_list = gen_random_clusters(num_clusters)
    scp_times = []
    fcp_times = []

    # measure run time of slow_closest_pair
    start_time_scp = time.time()
    slow_closest_pair(cluster_list)
    elapsed_time_scp = time.time() - start_time_scp
    scp_times.append(elapsed_time_scp)

    # measure run time of fast_closest_pair
    start_time_fcp = time.time()
    fast_closest_pair(cluster_list)
    elapsed_time_fcp = time.time() - start_time_fcp
    fcp_times.append(elapsed_time_fcp)

    # print "\n-------------------------------------------"
    # print "number of clusters: ", num_clusters
    # print "slow_closest_pair elapsed_time:", elapsed_time_scp
    # print "fast_closest_pair elapsed_time:", elapsed_time_fcp
    # print "-------------------------------------------"
    return [scp_times, fcp_times]


def plot_runtimes(num_clusters_range):
    """ plots computed runtimes for slow and fast closest pair algorithms """
    scp_times = []
    fcp_times = []

    for num in range(num_clusters_range[0], num_clusters_range[1]+1):
        result = compute_runtimes(num)
        scp_times.append(result[0])
        fcp_times.append(result[1])

    print "\n\nscp_times:", scp_times
    print "fcp_times:", fcp_times

    # plot n(x) vs time (y) on a standard plot
    xvals = range(num_clusters_range[0], num_clusters_range[1]+1)
    yvals1 = scp_times
    yvals2 = fcp_times

    plt.plot(xvals, yvals1, '-b', label='slow_closest_pair')
    plt.plot(xvals, yvals2, '-r', label='fast_closest_pair')
    plt.xlabel('number of initial clusters')
    plt.ylabel('run time (seconds)')
    plt.legend(loc='upper right')
    plt.show()

# compute_runtimes(200)
# num_clusters_range = [2, 200]
# plot_runtimes(num_clusters_range)


#########################################################
# Question #2 (1 pt)
# Use alg_project3_viz to create an image of the 15 clusters generated by applying hierarchical clustering to the 3108 county cancer risk data set. You may submit an image with the 3108 counties colored by clusters or an enhanced visualization with the original counties colored by cluster and linked to the center of their corresponding clusters by lines. You can generate such an enhanced plot using our alg_clusters_matplotlib code by modifying the last parameter of plot_clusters to be True. Note that plotting only the resulting cluster centers is not acceptable.
#  SEE alg_project3_viz.py

