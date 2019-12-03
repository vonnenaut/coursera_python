def triangular_sum(num):
	""" 
	Computes arithmetic sum of num
	"""
	if num == 0:
		return 0
	else:		
		return num + triangular_sum(num - 1)
	

print triangular_sum(3)