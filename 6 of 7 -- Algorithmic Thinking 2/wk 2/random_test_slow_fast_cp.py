import random, alg_cluster
import closest_pair_functions as cpf

def random_test(num):
    for _ in range(num):
        cluster_list = []
        for i in range(50): # The number of clusters
            cluster_list.append(alg_cluster.Cluster(set([str(i)]), 100.0*random.random(), 100.0*random.random(), random.random(), random.random()))
        cluster_list.sort(key = lambda cluster: cluster.horiz_center())
        if cpf.slow_closest_pair(cluster_list) != cpf.fast_closest_pair(cluster_list):
            print cluster_list
            print cpf.slow_closest_pair(cluster_list)
            print cpf.fast_closest_pair(cluster_list)
            break
    print "The results match."
    
random_test(500) # take a few seconds with desktop python