""" Recursive Fibonacci Sequence calculator
	Note:  This version can be improved via
			memoization (reduces repeated work)
"""
def fibonacci(place):
	""" calculates Fibonacci sequence to given place
	"""
	# handle base cases
	if place == 0:
		return 0
	elif place == 1:
		return 1
	else:	# breka problem down into smaller steps
		return fibonacci(place-1) + fibonacci(place-2)

# Test
for number in range(20):
	print fibonacci(number)