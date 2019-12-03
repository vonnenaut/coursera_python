
"""
Algorithmic Thinking 2
wk 1 Quiz

list comprehensions:
variable2 = [f(variable1) : variable1 in iterable (and restriction on variable1)]
"""

# 1.  How many inversions in 
# A = [5, 4, 3, 6, 7] ?
import random

def array_maker(size):
	""" creates an array of somewhat random values of a given size """
	new_array =[]
	for dummy_idx in range(size):
		value = random.randrange(size * 100)
		new_array.append(value)
	return new_array


def num_inversions(array):
	""" returns count of number of inversions in an array """
	inversions = []
	for index_i in range(len(array)):
		for index_j in range(len(array)):
			if array[index_i] > array[index_j] and index_i < index_j:
				inversions.append((array[index_i], array[index_j]))
	# print "inversions:", inversions
	# print "len(inversions):", len(inversions)
	return len(inversions)

array = range(3, 0, -1)
print "n = %r" % (len(array))
print "number of inversions:", num_inversions(array)
print

array = range(4, 0, -1)
print "n = %r" % (len(array))
print "number of inversions:", num_inversions(array)
print

array = range(5, 0, -1)
print "n = %r" % (len(array))
print "number of inversions:", num_inversions(array)
print

array = range(6, 0, -1)
print "n = %r" % (len(array))
print "number of inversions:", num_inversions(array)
print



value = 10
for number in range(value, 200, value*2):
	value = value*2
	array = range(number, 0, -1)
	print "n = %r" % (len(array))
	print "number of inversions:", num_inversions(array)
	print

# array = range(10, 0, -1)
# print "n = %r" % (len(array))
# print "number of inversions:", num_inversions(array)
# print

# array = range(30, 0, -1)
# print "n = %r" % (len(array))
# print "number of inversions:", num_inversions(array)
# print

# array = range(30, 0, -1)
# print "n = %r" % (len(array))
# print "number of inversions:", num_inversions(array)
# print

# array = array_maker(10)
# print "\narray:", array
# print "len(array):", len(array)
# print "num_inversions(array):", num_inversions(array)

# array = array_maker(30)
# print "\nlen(array):", len(array)
# print "num_inversions(array):", num_inversions(array)

# array = array_maker(100)
# print "\nlen(array):", len(array)
# print "num_inversions(array):", num_inversions(array)

# array = array_maker(500)
# print "\nlen(array):", len(array)
# print "num_inversions(array):", num_inversions(array)