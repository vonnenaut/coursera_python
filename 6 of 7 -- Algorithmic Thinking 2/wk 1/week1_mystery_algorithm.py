""" week1_mystery algorithm implementation """

def Mystery(sorted_array, left_bound, right_bound):
	""" mystery function """
	if left_bound > right_bound:
		print "case 1"
		return -1;

	m = (left_bound + right_bound)/2
	if sorted_array[m] == m:
		print "case 2"
		return m
	else:
		if sorted_array[m] < m:
			print "case 3"
			return Mystery(sorted_array, m + 1, right_bound)
		else:
			print "case 4"
			return Mystery(sorted_array, left_bound, m - 1)

# print "\n"
# array = [1, 2, 3]
# print "array =", array 
# left_bound = 0
# right_bound = 2
# print "Mystery(%r, %r):\n%r" % (left_bound, right_bound, Mystery(array, left_bound, right_bound))
# print "\n"
 
# Mystery([-2,0,1,3,7,12,15],0,6)
print "\n"
array = [-2,0,1,3,7,12,15]
print "array =", array 
left_bound = 0
right_bound = 6
print "Mystery(%r, %r):\n%r" % (left_bound, right_bound, Mystery(array, left_bound, right_bound))
print "\n"

# print "\n"
# print "array = [1, 2, 3, 4]"
# array = [1, 2, 3, 4]
# print "Mystery(array, 0, 2):", Mystery(array, 0, 2)
# print "\n"
