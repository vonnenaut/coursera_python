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
import math, random, time, alg_cluster, copy
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
    indices = []   

    # Let S be a list of the set {i: |xi - mid| < half_width}
    # print "\ncp_strip horiz_center:", horiz_center
    indices = [index for index in range(len(cluster_list)) if abs(cluster_list[index].horiz_center()-horiz_center)<=half_width]
    
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
    new_cluster_list = copy.deepcopy(cluster_list)

    # for index in range(len_cluster_list):
    #     new_cluster_list.append(alg_cluster.Cluster(set(cluster_list[index].fips_codes()), cluster_list[index].horiz_center(), cluster_list[index].vert_center(), cluster_list[index].total_population(), cluster_list[index].averaged_risk()))

    # while |C| > k do
    while len(new_cluster_list) > num_clusters:
        # (Ci,Cj) <-- argminCi,Cj Element C, i != j^dCi,Cj;
        # C <-- C Union {Ci Union Cj};  // line 5
        # C <-- C \ {Ci, Cj};             // line 6
        # need to sort cluster list before passing to fast_closest_pair
        new_cluster_list.sort(key=lambda cluster: cluster.horiz_center())
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
    Output:   A set C of k clusters that provides a clustering of the points in P.
    """
    # print "\n\ncluster_list:", cluster_list
    # print "\n\nnum_clusters:", num_clusters
    # print "num_iterations:", num_iterations, "\n"
    points = cluster_list[:]
    
    # n <-- |p|;
    len_points_list = len(points)

    # position initial clusters at the location of clusters with largest populations (i.e., cluster[3] which is population) 
    # Cluster centers computed in lines 2 and 8-9 should stay fixed as lines 5-7 are executed during one iteration of the outer loop.  To avoid modifying these values during execution of lines 5-7,  you should consider storing these cluster centers in a separate data structure.
    cluster_centers = []
    temp_cl = points[:]
    
    temp_cl.sort(key=lambda cluster: cluster.total_population())
    # print "temp_cl:", temp_cl
    for cluster in reversed(temp_cl):
        if len(cluster_centers) < num_clusters:
            cluster_centers.append(alg_cluster.Cluster(set([]), cluster.horiz_center(), cluster.vert_center(), 0, 0))
    # print "\n\ncluster_centers:", cluster_centers, "\n\n"

    # For number of iterations
    # for i <-- 1 to q do
    for dummy_var in range(num_iterations):
        # initialize the new clusters to be empty, i.e., represent an empty cluster as a Cluster object whose set of counties is empty and whose total population is zero
        # initialize k (num_clusters) empty sets C1, ... Ck;
        cluster_groupings = []
        for index in range(len(cluster_centers)):
            # print "\n\ncluster_centers[index]:", cluster_centers[index], "\n\n"
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
                    
            # print "\n\n\n\npoints[index]:", points[index]
            # print "\nmin_dist:", min_dist
            # print "\ncluster_groupings[nearest_cluster_index]:", cluster_groupings[nearest_cluster_index]

            # Add the county to the corresponding new cluster
            # C sub L <-- C sub L Union {psub j};  // handled with Cluster class merge_clusters method, which will automatically update the cluster centers to correct locations.
            cluster_groupings[nearest_cluster_index].merge_clusters(points[index])
        # print "\n\n\n\ncluster_groupings:", cluster_groupings
        # Set old clusters equal to new clusters 
        # for f = 1 to k do
        for index in range(len(cluster_centers)):
            # muf = center (Cf)     // handled with Cluster class built-in method(s)
            cluster_centers[index] = cluster_groupings[index].copy()
        # print "\n\nupdated cluster_centers:", cluster_centers

    # return {C1, C2, ..., Ck};
    # Return the new clusters       
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


def compute_rt_hier_kmeans(num_clusters):
    """ computes run-times for hierarchical and k-means clustering algorithms """
    cluster_list = gen_random_clusters(num_clusters)
    hier_times = []
    kmeans_times = []
    num_iter = 3
    num_output_clusters = 5

    # measure run time of hierarchical clustering algorithm
    start_time_hier = time.time()
    hierarchical_clustering(cluster_list, num_output_clusters)
    elapsed_time_hier = time.time() - start_time_hier
    hier_times.append(elapsed_time_hier)

    # measure run time of k-means clustering algorithm
    start_time_kmeans = time.time()
    kmeans_clustering(cluster_list, num_output_clusters, num_iter)
    elapsed_time_kmeans = time.time() - start_time_kmeans
    kmeans_times.append(elapsed_time_kmeans)

    return [hier_times, kmeans_times]


def plot_runtimes(num_clusters_range, algo_type):
    """ if given a range, plots computed runtimes for slow and fast closest pair algorithms for question 1.
    If given a single value, plots computed runtimes for hierarchical and k-means clustering algorithms"""
    if algo_type == 1:
        scp_times = []
        fcp_times = []
        for num in range(num_clusters_range[0], num_clusters_range[1]+1):
            result = compute_runtimes(num)
            scp_times.append(result[0])
            fcp_times.append(result[1])
    elif algo_type == 2:
        hier_times = []
        kmeans_times = []
        num_output_clusters = 5
        for num in range(num_clusters_range[0], num_clusters_range[1]+1):
            result = compute_rt_hier_kmeans(num)
            hier_times.append(result[0])
            kmeans_times.append(result[1])

    # plot n(x) vs time (y) on a standard plot
    if algo_type == 1:
        xvals = range(num_clusters_range[0], num_clusters_range[1]+1)
        yvals1 = scp_times
        yvals2 = fcp_times
    
        plt.plot(xvals, yvals1, '-b', label='slow_closest_pair')
        plt.plot(xvals, yvals2, '-r', label='fast_closest_pair')
        plt.xlabel('number of initial clusters')
        plt.ylabel('run time (seconds)')
        plt.legend(loc='upper right')
        plt.title('Run-time of slow vs fast closest pair algorithms (desktop python)')
        plt.show()
    elif algo_type == 2:
        xvals = range(num_clusters_range[0], num_clusters_range[1]+1)
        yvals1 = hier_times
        yvals2 = kmeans_times
    
        plt.plot(xvals, yvals1, '-b', label='hierarchical_clustering')
        plt.plot(xvals, yvals2, '-r', label='kmeans_clustering')
        plt.xlabel('number of initial clusters')
        plt.ylabel('run time (seconds)')
        plt.legend(loc='upper right')
        plt.title('Run-time of slow vs fast closest pair algorithms (desktop python)')
        plt.show()

compute_runtimes(200)
num_clusters_range = [2, 200]
plot_runtimes(num_clusters_range, 1)


#########################################################
# Question #2 (1 pt)
# Use alg_project3_viz to create an image of the 15 clusters generated by applying hierarchical clustering to the 3108 county cancer risk data set. You may submit an image with the 3108 counties colored by clusters or an enhanced visualization with the original counties colored by cluster and linked to the center of their corresponding clusters by lines. You can generate such an enhanced plot using our alg_clusters_matplotlib code by modifying the last parameter of plot_clusters to be True. Note that plotting only the resulting cluster centers is not acceptable.
#  SEE alg_project3_viz.py


#########################################################
# Question #3 (1 pt)
# Use alg_project3_viz to create an image of the 15 clusters generated by applying hierarchical clustering to the 3108 county cancer risk data set. You may submit an image with the 3108 counties colored by clusters or an enhanced visualization with the original counties colored by cluster and linked to the center of their corresponding clusters by lines. You can generate such an enhanced plot using our alg_clusters_matplotlib code by modifying the last parameter of plot_clusters to be True. Note that plotting only the resulting cluster centers is not acceptable.
#  SEE alg_project3_viz.py


########################################################
# Question 4 (1 pt)

# Which clustering method is faster when the number of output clusters is either a small fixed number or a small fraction of the number of input clusters? Provide a short explanation in terms of the asymptotic running times of both methods. You should assume that hierarchical_clustering uses fast_closest_pair and that k-means clustering always uses a small fixed number of iterations.
# num_input_clusters = [10, 100]
# plot_runtimes(num_input_clusters, 2)

#  K-means clustering is faster.  When there is a really small number of input clusters, both running times are similar, but as the number of input clusters grows, the running time of hierarchical clustering increases rapidly and k-means doesn't increase much at all, staying nearly flat (horizontal) in a graph of initial clusters vs running time.


########################################################
# Question 5 (1 pt)
# Automation

# In the next five questions, we will compare the level of human supervision required for each method.
# Question 5 (1 pt)

# Use alg_project3_viz to create an image of the 9 clusters generated by applying hierarchical clustering to the 111 county cancer risk data set. You may submit an image with the 111 counties colored by clusters or an enhanced visualization with the original counties colored by cluster and linked to the center of their corresponding clusters by lines.

# Once you are satisfied with your image, upload your image in the peer assessment. Your submitted image will be assessed based on whether it matches our solution image. You do not need to include axes, axes labels, or a title for this image.
#  SEE alg_project3_viz.py


########################################################
# Question 6 (1 pt)

# Use alg_project3_viz to create an image of the 9 clusters generated by applying 5 iterations of k-means clustering to the 111 county cancer risk data set. You may submit an image with the 111 counties colored by clusters or an enhanced visualization with the original counties colored by cluster and linked to the center of their corresponding clusters by lines. As in Project 3, the initial clusters should correspond to the 9 counties with the largest populations.

# Once you are satisfied with your image, upload your image in the peer assessment. Your submitted image will be assessed based on whether it matches our solution image. You do not need to include axes, axes labels, or a title for this image.
#  SEE alg_project3_viz.py


########################################################
# Question 7 (1 pt)

# The clusterings that you computed in Questions 5 and 6 illustrate that not all clusterings are equal. In particular, some clusterings are better than others. One way to make this concept more precise is to formulate a mathematical measure of the error associated with a cluster. Given a cluster C, its error is the sum of the squares of the distances from each county in the cluster to the cluster's center, weighted by each county's population. If pi is the position of the county and wi is its population, the cluster's error is:

# where c is the center of the cluster C. The Cluster class includes a method cluster_error(data_table) that takes a Cluster object and the original data table associated with the counties in the cluster and computes the error associated with a given cluster.

# Given a list of clusters L, the distortion of the clustering is the sum of the errors associated with its clusters.

# Write a function compute_distortion(cluster_list) that takes a list of clusters and uses cluster_error to compute its distortion. Now, use compute_distortion to compute the distortions of the two clusterings in questions 5 and 6. Enter the values for the distortions (with at least four significant digits) for these two clusterings in the box below. Clearly indicate the clusterings to which each value corresponds.
#  SEE alg_project3_viz.py


########################################################
# Question 8 (1 pt)
# Examine the clusterings generated in Questions 5 and 6. In particular, focus your attention on the number and shape of the clusters located on the west coast of the USA.

# Describe the difference between the shapes of the clusters produced by these two methods on the west coast of the USA. What caused one method to produce a clustering with a much higher distortion? To help you answer this question, you should consider how k-means clustering generates its initial clustering in this case.

# In explaining your answer, you may need to review the geography of the west coast of the USA.
# 5 - Hierarchical (# Hierarchical_clustering error:  1.75163886916e+11)
# 6 - Kmeans  (# kmeans_clustering error:  5.67726966298e+11)
#
 
# Kmeans clustered counties/data points from a much wider geographic area on the west coast, for example, grouping WA, OR and northern CA counties into the same cluster.  This introduced greater distortion in the calculated clusters.  At the same time, two clusters were created very close to one another in southern CA and so choice of cluster groupings seems more problematic in kmeans clustering than hierarchical clustering.    

########################################################
# Question 9 (1 pt)

# Based on your answer to Question 8, which method (hierarchical clustering or k-means clustering) requires less human supervision to produce clusterings with relatively low distortion? 
#
# While it takes more time to run, hierarchical clustering requires less human supervision with relatively low

########################################################
# Question 10 (4 pts)
# Compute the distortion of the list of clusters produced by hierarchical clustering and k-means clustering (using 5 iterations) on the 111, 290, and 896 county data sets, respectively, where the number of output clusters ranges from 6 to 20 (inclusive).Important note:To compute the distortion for all 15 output clusterings produced by hierarchical_clustering, you should remember that you can use the hierarchical cluster of size 20 to compute the hierarchical clustering of size 19 and so on. Otherwise, you will introduce an unnecessary factor of 15 into the computation of the 15 hierarchical clusterings.

# Once you have computed these distortions for both clustering methods, create three separate plots (one for each data set) that compare the distortion of the clusterings produced by both methods. Each plot should include two curves drawn as line plots. The horizontal axis for each plot should indicate the number of output clusters while the vertical axis should indicate the distortion associated with each output clustering. For each plot, include a title that indicates the data set used in creating the plots and a legend that distinguishes the two curves.

# Once you are satisfied with your plots, upload these plots (separately) into the peer assessment. Your plots will be assessed based on the answers to the following questions:

#     Do the plots follow the formatting guidelines for plots? Does the title of each plot indicate which data was used to create the plot? Do the plots include a legend?
#      Do the two curves in each plot have the correct shapes?
#  SEE alg_project3_viz.py


########################################################
# Question 11(1 pt)
# For each data set (111, 290, and 896 counties), does one clustering method consistently produce lower distortion clusterings when the number of output clusters is in the range 6 to 20? Is so, indicate on which data set(s) one method is superior to the other. 
#
# For the 111-county data set, k-means clustering consistently produces lower distortion clusterings in the range of 6 to 20 output clusters, but for the 290- and 896- county data sets, hierarchical clustering produces lower distortion.


########################################################
# Question 12(0 pts)
# Which clustering method would you prefer when analyzing these data sets? Provide a summary of each method's strengths and weaknesses on these data sets in the three areas considered in this application. Your summary should be at least a paragraph in length (4 sentences minimum). 
# Because I value accuracy and less required intervention over time saved, hierarchical clustering is my preferred clustering method for analyzing data sets.  Hierarchical's strength is its accuracy without need of manual intervention.  It's weakness is the running time required on large data sets.  K-means' strength is is running time, which is quite a bit faster than hierarchical with large data sets, but its weakeness is its relatively higher level of inaccuracy and so it would require more manual intervention reducing its potential for automation.  This decreased ability to be run in an automated fashion would increase time and expenses for paying individuals to analyze data.  For extremely large data sets, I'd rather not rely on human intervention which introduces human error and unknown increases in time spent on such.