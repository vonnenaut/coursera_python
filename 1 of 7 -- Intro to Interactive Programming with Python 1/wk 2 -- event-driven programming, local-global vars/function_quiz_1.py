def f_of_x(x):
	func = (-5*(x**5)) + 69*(x**2) - 47
	return func

for x in range(4):
	print "f(%s): " % (str(x))
	print f_of_x(x)
	print "\n"
