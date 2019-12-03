def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.  

    Algorithm 5:  ClosestPairStrip
    Input:  A set P of points whose ith point, pi, is a pair (xi, yi); mid and w, both of which are real numbers.
    Output:  A tuple (d,i,j) where d is the smallest pairwise distane of points in P whose horizontal (x) coordinates are within w from mid.

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

    # FOR TESTING PURPOSES -------------------
    print "\n\n--------------------- Distances --------------------- "
    for index1 in range(len(cluster_list)):
        for index2 in range(1, len(cluster_list)):
            if index1 != index2:
                print "*****"
                print "\n\nclusters: [%r, %r]  distance: %r" % (index1, index2, cluster_list[index1].distance(cluster_list[index2]))
                print "\ncluster %r: %r" % (index1, cluster_list[index1])
                print "\ncluster %r: %r \n\n" % (index2, cluster_list[index2])
                print "*****"
    print "----------------------- ----------------------- \n\n"
    # END TESTING CODE -----------------------

    # Let S be a list of the set {i: |xi - mid| < half_width}
    # for index in range(len(cl_copy)):
    #   print "abs(cl_copy[%r].horiz_center()-horiz_center) < half_width: %r" % (index, abs(cl_copy[index].horiz_center()-horiz_center) < half_width)
    #   if abs(cl_copy[index].horiz_center()-horiz_center) < half_width:
    #       indices.append(index)
    indices = [index for index in range(len(cluster_list)) if abs(cl_copy[index].horiz_center()-horiz_center)<half_width]
    
    print "\n\n/////////////"
    print "indices:", indices
    print "/////////////\n"

    print "Clusters:\n-------"
    for cluster in cl_copy:
        print cluster

    #  NOTE:  Let's not do this and say we did.  It has no benefit to follow the pseudocode and causes problems.  Instead, sort at the end before returning. 
    # Sort the indices in S in nondecreasing order of the vertial (y) coordinates of their associated points;
    # cl_copy.sort(key = lambda cluster: cluster.vert_center())
    # print "\n\nClusters (sorted vertically):\n-------"
    # for cluster in cl_copy:
    #   print cluster

    # k <-- length(S);
    len_indices = len(indices)

    # (d,i,j) <-- (infinity, -1, -1);
    output_list = [99999.9, -1, -1]
        
    # for u <-- 0 to k - 2 do
    for value1 in range(len_indices):
        #   for v <-- u + 1 to min{u+3,k-1} do
        for value2 in range(value1+1, min(value1+3,len_indices)):
            # print "\n\n**pair_distance indices[value1]: %r   indices[value2]: %r  %r **\n\n" % (indices[value1], indices[value2], pair_distance(cl_copy,indices[value1],indices[value2]))
            # print "cl_copy[%r]: %r" % (indices[value1], cl_copy[indices[value1]])
            # print "cl_copy[%r]: %r" % (indices[value2], cl_copy[indices[value2]])
            # print
            # (d,i,j) <-- min{(d,i,j),(dsub(psubS[u],PsubS[v]), S[u],S[v])}
            min_dist = min(output_list[0], pair_distance(cl_copy,indices[value1],indices[value2])[0])
            if output_list[0] != min_dist:
                output_list = [pair_distance(cl_copy,indices[value1],indices[value2])[0], indices[value1], indices[value2]]
            # output_list = min(output_list,(pair_distance(cl_copy,indices[value1],indices[value2]),indices[value1],indices[value2]))

    # return(d,i,j)
    print "\n\n\n############################\n\tResults\n############################\n"
    print "\ncluster_list:", cluster_list
    print "\nhoriz_center:", horiz_center
    print "half_width:", half_width, "\n"
    print "output_list:", output_list, "\n"
    return tuple(output_list)