""" 
Algorithmic Thinking 2
Week 2 Project (#3)
Implement and Assess 2 Methods for Clustering Data
and implementing 
2 methods for computing closest pairs
and 
2 methods for clustering data

Center of a cluster Csub u:
center(C sub u) = 1/ length(C sub u) * Summation of p sub i element of C sub u (xi, yi)
ex. -- if C sub u = {p1, p2, p3} 
with p1 = (1,2), p2 = (4,6), p3 = (4,4)
center(C sub u) = 1/3 ((1,2) + (4,6) + (4,4)) = 1/3 (9,12) = (3,4)

-------------------
Algorithm 1: Hierarchical Clustering
Input:  A set P of points wose ith point, pi is a pair (xi, yi); k, the desired number of clusters.
Output:  A set C of k clusters that provides a clustering of the points in P.

n <-- |P|
Initialize n clusters C = {C1, ... Cn} such that Ci = {pi};
while |C| > k do
	(Ci,Cj) <-- argminCi,Cj Element C, i != j^dCi,Cj;
	C <-- C Union {Ci Union Cj};
	C <-- C \ {Ci, Cj};
return C;



Algorithm 2:  KMeansClustering
Input:  A set P of points whose ith point, pi, is a pair (xi, yi); k, the desired number of clusters, q, a number of iterations.
Output:   A set C of k clusters that provides a clustering fo the points in P.

n <-- |p|;
Initialize k centers mu1, ..., muk to initial values (each mu is a point in the 2D space);
for i <-- 1 to q do
	initialize k empty sets C1, ... Ck;
	for j = 0 to n - 1 do
		L <-- argmin1 <= f <=k^dsub pj, mu sub f
		C sub L <-- C sub L Union {psub j};
	for f = 1 to k do
		muf = center (Cf)
return {C1, C2, ..., Ck};

----------------------------------------
Distance Between Points and Clusters (Error)

Both algorithms use a distance measure, d.
It's used directly in KMeansClustering.

Distance measure:
 dpi,pj = sqrt((xi-xj)^2 + (yi - yj)^2)

It's used via the centers in HierarchicalClustering:
dCi,Cj = dcenter(C1),center(Cj)


We assumed the # of clusters is known.  When it's not, we can determine it by varying the value of k (k=1,23 ...,) and for each value of k, inspect the quality of the clusters obtained (error of a cluster, reflecting how tightly packed around the center the cluster's points are.)

Error of a Cluster:
	error(Ci) = Summation p element Ci of (dp, center(Ci))^2

--------------------------------
Closest Pair Problem -- find two clusters closest to one another (HierarchicalClustering).


Algorithm 3:  SlowClosestPair
Input:  A set P of (>=2) points whose ith point, pi, is a pair (xi, yi).
Output:  A tuple (d,i,j) where d is the smallest pairwise distance of points in P and i,j are the indices of two points whose distance is d.

(d,i,j) <-- (infinity, -1, -1);
foreach pu Element of P do
	foreach pv Element of P (u != v) do
		(d,i,j) <-- min{(d,i,j), (d sub(pu,pv),u,v)};  // min compares the first element of each tuple

return(d,i,j);


Algorithm 4:  FastClosestPair (Divide and Conquer)
Input:  A set P of (>=2) points whose ith point, pi is a pair(xi,yi), sorted in nondecreasing order of their horizontal (x) coordinates.
Output:  A tuple (d,i,j) where d is the smallest pairwise distance of the points in P, and i,j are the indices of two points whose distance is d.

n <-- length(P);
if n <= 3 then
	(d,i,j) <== SlowClosestPair(P);
else
	m <-- leftbracketwithouttop n/2 rightbracketwithouttop
	Psub L <-- {pi: 0 <= i <= m-1}; Pr <--{pi: m <= i <= n-1};  // Psub L and Pr are also sorted
	(dL, iL, jL) <-- FastClosestPair(PL);
	(dr, ir, jr) <-- FastClosestPair(Pr);
	(d,i,j) <-- min{(dL,iL,jL), (dr,ir+m,jr+m)};
	mid <-- 1/2(x sub m-1 + x sub m)		// center line of strip
	(d,i,j) <- min{(d,i,j), ClosestPairStrip(P, mid, d)}
return(d,i,j);


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

