rest_strings = []

def gen_all_strings(word):
	"""
	recursively generates all possible enumerations of the letters of a word
	Generate all strings that can be composed from the letters in word in any order.
    Returns a list of all strings that can be formed from the letters in word.  This function should be recursive.   
    # 1. Split the input word into two parts: the first 
    # character (first) and the remaining part (rest).
    # 2. Use gen_all_strings to generate all appropriate 
    # strings for rest. Call this list rest_strings.
    # 3. For each string in rest_strings, generate new strings by 
    # inserting the initial character, first, in all possible 
    # positions within the string.
    # 4. Return a list containing the strings in rest_strings 
    # as well as the new strings generated in step 3.
	"""
	global rest_strings
	# base case
	if len(word) <= 1:
		# rest_strings.append(word)
		return ['', word]
	else:	# recursive case
		first = word[0]
		rest = word[1:]

		for index in range(len(rest)+1):
			rest_strings.append(rest[:index]+first+rest[index:])

		gen_all_strings(rest)
	return rest_strings + list('') + list(word)

word = "bin"
print gen_all_strings(word)

# Expected output:
# ['', 'b', 'i', 'n', 'in', 'ni', 'bin', 'ibn', 'inb', 'bi', 'ib', 'bni', 'nbi', 'nib']

# Actual output (this version):
# ['bin', 'ibn', 'inb', 'in', 'ni', 'b', 'i', 'n']
# Actual output (word_wrangler version):
# ['', 'bin', 'in', 'i', 'ni', 'b', 'ibn', 'inb', 'bi', 'ib', 'bni', 'nbi', 'nib']
