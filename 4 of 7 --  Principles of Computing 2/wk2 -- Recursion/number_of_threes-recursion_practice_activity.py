"""
Write a function number_of_threes(num) that returns the number of times the digit 3 appears in the decimal representation of the non-negative integer num. For example number_of_threes(34534) should return 2.
"""

# def number_of_threes(num):
# 	""" returns number of times the digit
# 	three appears in num
# 	"""
# 	if "3" not in str(num):
# 		return 0
# 	else:
# 		number = 0
# 		for char in str(num):
# 			if char is "3":
# 				number += 1
# 	return number

def number_of_threes(num):
	""" returns number of times the digit
 	three appears in num
 	"""
 	if num == 0:
 		return 0
 	else:
 		unit_digit = num % 10
 		threes_in_rest = number_of_threes(num // 10)
 		if unit_digit == 3:
 			return threes_in_rest + 1
 		else:
 			return threes_in_rest


print number_of_threes(333)
print number_of_threes(6541)
print number_of_threes(354300321)
