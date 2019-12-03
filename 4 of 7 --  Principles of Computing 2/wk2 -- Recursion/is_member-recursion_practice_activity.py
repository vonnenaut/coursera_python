"""
Write a function is_member(my_list, elem) that returns True if elem is a member of my_list and False otherwise. For example, is_member(['c', 'a', 't'], 'a') should return True. Do not use any of Python's built-in list methods or an operator like in.
"""

def is_member(my_list, elem):
	# handle base case
	if my_list == []:
		return False
	else:	# break problem down into smaller steps
		first_element = my_list[0]
		if first_element == elem:
			return True
		else:
			return is_member(my_list[1:], elem)

print is_member([1,2,3], 3)
print is_member([0, 9, 7], 3)
print is_member([], 2)
