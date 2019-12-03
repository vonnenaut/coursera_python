"""
Example code for creating and visualizing
cluster of county-based cancer risk data

Note that you must download the file
http://www.codeskulptor.org/#alg_clusters_matplotlib.py
to use the matplotlib version of this code
"""

# Flavor of Python - desktop or CodeSkulptor
DESKTOP = True

import math, random, urllib2, requests, alg_cluster
from requests.exceptions import HTTPError
import matplotlib.pyplot as plt

# conditional imports
if DESKTOP:
    import closest_pair_functions as cpf     # desktop project solution
    import alg_clusters_matplotlib
else:
    #import http://www.codeskulptor.org/#user43_FygdmrDYIh_0.py   # CodeSkulptor project solution
    import alg_clusters_simplegui
    import codeskulptor
    codeskulptor.set_timeout(30)


###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"


def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    try:
        data_file = urllib2.urlopen(data_url)
    except HTTPError:
        print "Could not load data from URL:  ", data_url

    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]


############################################################
# Code to create sequential clustering
# Create alphabetical clusters for county data

def sequential_clustering(singleton_list, num_clusters):
    """
    Take a data table and create a list of clusters
    by partitioning the table into clusters based on its ordering
    
    Note that method may return num_clusters or num_clusters + 1 final clusters
    """
    
    cluster_list = []
    cluster_idx = 0
    total_clusters = len(singleton_list)
    cluster_size = float(total_clusters)  / num_clusters
    
    for cluster_idx in range(len(singleton_list)):
        new_cluster = singleton_list[cluster_idx]
        if math.floor(cluster_idx / cluster_size) != \
           math.floor((cluster_idx - 1) / cluster_size):
            cluster_list.append(new_cluster)
        else:
            cluster_list[-1] = cluster_list[-1].merge_clusters(new_cluster)
            
    return cluster_list
                

#####################################################################
# Code to load cancer data, compute a clustering and 
# visualize the results


def run_example():
    """
    Load a data table, compute a list of clusters and 
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    data_table = load_data_table(DATA_3108_URL)
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
        
    cluster_list = sequential_clustering(singleton_list, 15)	
    print "Displaying", len(cluster_list), "sequential clusters"

    #cluster_list = cpf.hierarchical_clustering(singleton_list, 9)
    #print "Displaying", len(cluster_list), "hierarchical clusters"

    #cluster_list = cpf.kmeans_clustering(singleton_list, 9, 5)	
    #print "Displaying", len(cluster_list), "k-means clusters"

            
    # draw the clusters using matplotlib or simplegui
    if DESKTOP:
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, False)
        #alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)  #add cluster centers
    else:
        alg_clusters_simplegui.PlotClusters(data_table, cluster_list)   # use toggle in GUI to add cluster centers


def run_question(number, data_set):
    """
    Load a data table, compute a list of clusters and 
    plot a list of clusters.
    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    global DESKTOP
    print "Loading data table ..."
    data_table = load_data_table(data_set)
    print "Data table loaded.  Creating clusters ..."
    singleton_list = []

    # set correct number of clusters
    if number in [2, 3]:
        num_clusters = 15
    elif number in [5, 6]:
        num_clusters = 9
    print "\nQuestion number:  ", number
    print "Number of clusters to be calculated:  ", num_clusters

    # parse data_table into cluster objects
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    print "\nCluster list created.  Passing list to hierarchical_clustering ..."
        
    # calculate clusters
    if number == 0:
        cluster_list = sequential_clustering(singleton_list, 15)
        print "Displaying", len(cluster_list), "sequential clusters"
    elif number in [2, 5]:
        cluster_list = cpf.hierarchical_clustering(singleton_list, num_clusters)
        print "Displaying", len(cluster_list), "hierarchical clusters"
    elif number in [3, 6]:
        cluster_list = cpf.kmeans_clustering(singleton_list, num_clusters, 5)   
        print "Displaying", len(cluster_list), "k-means clusters"
    else:
        "Please pass a valid number to run_question.  Valid options are 0, 2, 3, 5, or 6."

            
    # draw the clusters using matplotlib or simplegui
    if DESKTOP:
        # alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, False)
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)  #add cluster centers
    else:
        alg_clusters_simplegui.PlotClusters(data_table, cluster_list)   # use toggle in GUI to add cluster centers


def compute_distortion(cluster_list):
    """ takes a list of clusters and uses cluster_error to compute its distortion """
    # use compute_distortion to compute the distortions of the two clusterings in questions 5 and 6
    num_clusters = 9
    num_iterations = 5
    hier_list = []
    kmeans_list = []

    # load data table
    data_table = load_data_table(DATA_111_URL)
 
    hier_list = cpf.hierarchical_clustering(cluster_list, num_clusters)
    hier_error = 0
    for cluster in hier_list:
        hier_error += cluster.cluster_error(data_table)
    
    kmeans_list = cpf.kmeans_clustering(cluster_list, num_clusters, num_iterations) 
    kmeans_error = 0
    for cluster in kmeans_list:
        kmeans_error += cluster.cluster_error(data_table)

    print "\n\n\n\n-------- -------- Results -------- --------"
    print "Number of clusters:  %r" % num_clusters
    print "hierarchical_clustering error: ", hier_error
    print "kmeans_clustering error: ", kmeans_error
    print "----- ----- ----- ----- ----- ----- -----"
    return [hier_error, kmeans_error]


def compute_distortion_plot_helper(cluster_list, data_table, num_clusters):
    """ takes a list of clusters and uses cluster_error to compute its distortion """
    # use compute_distortion to compute the distortions of the two clusterings in questions 5 and 6
    num_iterations = 5
    hier_list = []
    kmeans_list = []
 
    hier_list = cpf.hierarchical_clustering(cluster_list, num_clusters)
    hier_error = 0
    for cluster in hier_list:
        hier_error += cluster.cluster_error(data_table)
    
    kmeans_list = cpf.kmeans_clustering(cluster_list, num_clusters, num_iterations) 
    kmeans_error = 0
    for cluster in kmeans_list:
        kmeans_error += cluster.cluster_error(data_table)

    # print "\n\n\n\n-------- -------- Results -------- --------"
    # print "Number of clusters:  %r" % num_clusters
    # print "hierarchical_clustering error: ", hier_error
    # print "kmeans_clustering error: ", kmeans_error
    # print "----- ----- ----- ----- ----- ----- -----"
    return [hier_error, kmeans_error]


def plot_distortions():
    """ The horizontal axis for each plot should indicate the number of output clusters while the vertical axis should indicate the distortion associated with each output clustering."""
    num_clusters = [6, 20]
    singleton_list = []
    distortions = []
    dist_hier = []
    dist_kmeans = []

    # prepare clusters from data table
    print "Loading data table ..."
    # change the following line to match desired data set, i.e., DATA_111_URL, DATA_290_URL or DATA_896_URL
    data_table =  load_data_table(DATA_111_URL)
    print "Data table loaded.  Creating clusters ..."
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

    # calculate distortion for each value of output clusters in range 6 to 20
    for num in range(num_clusters[0], num_clusters[1]+1):
        distortions.append(compute_distortion_plot_helper(singleton_list, data_table, num))

    for dist in distortions:
        dist_hier.append(dist[0])
        dist_kmeans.append(dist[1])

    # # plot number of output clusters (x) vs distortion (y) for both hierarchical and kmeans on a standard plot
    xvals = range(num_clusters[0], num_clusters[1]+1)
    yvals1 = dist_hier
    yvals2 = dist_kmeans
    
    plt.plot(xvals, yvals1, '-b', label='hierarchical distortion')
    plt.plot(xvals, yvals2, '-g', label='kmeans distortion')
    plt.xlabel('number of final clusters')
    plt.ylabel('distortion')
    plt.legend(loc='upper right')
    plt.title('Num. Clusters vs Distortion (Hierarchical, K-means Algo. 111-set)')
    plt.show()
    

############################################################    
# Questions 2, 3, 5, 6
# run_example()
# run_question(2, DATA_3108_URL)
# run_question(3, DATA_3108_URL)
# run_question(5, DATA_111_URL)
# run_question(6, DATA_111_URL)


############################################################
# Question 7
# Loading data table ...
# Loaded 111 data points
# Data table loaded.  Creating clusters ...
# Loaded 111 data points
# Cluster list created.  Passing list to hierarchical_clustering ...
# Computing distortion on  9 hierarchical clusters
# Passing list to kmeans_clustering ...
# Computing distortion on  9 k-means clusters
# Hierarchical_clustering error:  1.75163886916e+11
# kmeans_clustering error:  5.67726966298e+11
# None
# -------- -------- Results -------- --------
# Number of clusters:  9
# hierarchical_clustering error:  1.75163886916e+11
# kmeans_clustering error:  2.71254226924e+11
# ----- ----- ----- ----- ----- ----- -----
#
# load data table
# data_table = load_data_table(DATA_111_URL)

# # parse data_table into cluster objects
# singleton_list = []
# for line in data_table:
#     singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4])) 

# compute_distortion(singleton_list)


############################################################
# Question 10 (4 pts)


# compute and plot distortions for range of output clusters (6 - 20) for both hierarchical and kmeans algorithms
# for line in data_table:
#     singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
# for value in range(num_output_clusters[0], num_output_clusters[1]+1):
#     distortions.append(compute_distortion(singleton_list))

# create 3 plots, one for each data set (111, 290 and 896)
# plot #1:  111 for hierarchical and kmeans
# plot #2:  290
# plot #3:  896
plot_distortions()

