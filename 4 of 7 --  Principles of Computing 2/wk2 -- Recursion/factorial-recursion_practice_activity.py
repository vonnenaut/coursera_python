def factorial(input):
	""" 
	calculate factorial of an input recursively
	"""
	# handle base case
	if input < 2:
		return 1
	else:	# break problem down into subproblems
		return input * factorial(input - 1)

# Test
input = 6
print str(input), "! is", factorial(input)
