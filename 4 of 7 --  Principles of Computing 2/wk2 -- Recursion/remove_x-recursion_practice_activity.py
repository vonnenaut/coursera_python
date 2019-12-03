"""
Write a function remove_x(my_string) that takes the string my_string and deletes all occurrences of the character 'x' from this string. For example, remove_x("catxxdogx") should return "catdog". You should not use Python's built-in string methods.
"""
def remove_x(my_string):
	# handle base case
	if my_string == "":
		return ""
	else:	# break problem down into smaller sub-problems
		first_char = my_string[0]
		rest_removed = remove_x(my_string[1:])
		if first_char == 'x':
			return rest_removed
		else:
			return first_char + rest_removed
print remove_x("sxnxoxrxkxexl")
print remove_x("catxxxbirdxxxdog")