""" 
Algorithic Thinking 2
Week 4 Application 4

In Project 4, we will implement four functions. The first pair of functions will return matrices that we will use in computing the alignment of two sequences. The second pair of functions will return global and local alignments of two input sequences based on a provided alignment matrix. You will then use these functions in Application 4 to analyze two problems involving comparison of similar sequences.


Modeling matrices

For Project 4, you will work with two types of matrices: alignment matrices and scoring matrices. Alignment matrices will follow the same indexing scheme that we used for grids in "Principles of Computing". Entries in the alignment matrix will be indexed by their row and column with these integer indices starting at zero. We will model these matrices as lists of lists in Python and can access a particular entry via an expression of the form alignment_matrix[row][col].

For scoring matrices, we take a different approach since the rows and the columns of the matrix are indexed by characters in Epsilon in union with '-'. In particular, we will represent a scoring matrix in Python as a dictionary of dictionaries. Given two characters row_char and col_char, we can access the matrix entry corresponding to this pair of characters via scoring_matrix[row_char][col_char].
"""
# import poc_simpletest as test

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """ builds a scoring matrix using alphabet of letters and scoring for diagonals (identicals), off-diagonals (unlike letters) and dashes (one dash in pair) """
    alphabet_list = []
    scoring_matrix = {}
    temp_vals = {}

    for letter in alphabet:
        alphabet_list.append(letter)
    alphabet_list.append('-')
    len_alpha = len(alphabet_list)

    for idx1 in range(len_alpha):
    	for idx2 in range(len_alpha):
    		if alphabet_list[idx1] == alphabet_list[idx2] and alphabet_list[idx1] != '-':
    			temp_vals[alphabet_list[idx2]] = diag_score
    		elif alphabet_list[idx1] != alphabet_list[idx2] and '-' not in [alphabet_list[idx1], alphabet_list[idx2]]:
    			temp_vals[alphabet_list[idx2]] = off_diag_score
    		elif '-' in [alphabet_list[idx1], alphabet_list[idx2]]:
    			temp_vals[alphabet_list[idx2]] = dash_score
    	# write temp value to scoring_matrix
    	scoring_matrix[alphabet_list[idx1]] = temp_vals
    	temp_vals = {}

    return scoring_matrix
    

def test_build_scoring_matrix():
	""" tests build_scoring_matrix """
	alphabet = set(['A', 'C', 'T', 'G'])
	diag_score = 10
	off_diag_score = 5
	dash_score = 0

	print build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score)


def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """ 
    Input:  Sequences X and Y and scoring matrix M.
    Output:  Dynamic programming (DP) table S

    computes either a global alignment matrix or a local alignment matrix depending on the value of global_flag True -- Q. 8, False -- Q. 12

    pseudocode (True, Q. 8):

    m <--|X|;   n <-- |Y|;    
    S[0,0] <-- 0;

    for i <-- 1 to m do
        S[i,0] <--- S[i-1,0] + Msub(Xsub(i-1), -)
    for j <-- 1 to n do
        S[0,j] <-- S[0,j-1] + Msub(-,Ysubj-1)
    for i <-- 1 to m do
        for j <-- 1 to n do
            S[i,j] <-- max(S[i-1,j-1] + Msub(Xsub(i-1),Ysub(j-1)),
                           S[i-1,j] + MsubXsub(i-1),-
                           S[i,j-1] + M-,Ysub(j-1)
    return S

    pseudocode (False, Q. 12) -- same but then converts negative values to zero

    """
    num_rows = len(seq_x)+1
    num_cols = len(seq_y)+1
    dp_table = [[0 for col in range(num_cols)] for row in range(num_rows)]

    for row in range(1,num_rows):
    	if not global_flag and dp_table[row-1][0] < 0:
    		    dp_table[row-1][0] = 0
        dp_table[row][0] = dp_table[row-1][0] + scoring_matrix[seq_x[row-1]]['-']
        if not global_flag and dp_table[row][0] < 0:
        	dp_table[row][0] = 0

    for col in range(1,num_cols):
    	if not global_flag and dp_table[0][col-1] < 0:
    		dp_table[0][col-1] = 0
    	dp_table[0][col] = dp_table[0][col-1] + scoring_matrix['-'][seq_y[col-1]]
    	if not global_flag and dp_table[0][col] < 0:
    		dp_table[0][col] = 0

    print "dp_table:", dp_table
    for row in range(1,num_rows):
    	for col in range(1,num_cols):
    		dp_table[row][col] = max(dp_table[row-1][col-1]+scoring_matrix[seq_x[row-1]][seq_y[col-1]], dp_table[row-1][col]+scoring_matrix[seq_x[row-1]]['-'], dp_table[row][col-1]+scoring_matrix['-'][seq_y[col-1]])
    		if not global_flag and dp_table[row][col] < 0:
    			dp_table[row][col] = 0

    return dp_table


# def test_compute_alignment_matrix():
# 	""" tests compute_alignment_matrix and uses build_scoring_matrix """
# 	tester = test.TestSuite()
# 	seq_x = ['AC', 'AC', 'ATG', 'CATG']
# 	seq_y = ['T', 'TAC', 'GATG', 'GATG']
# 	expected = [5, 20, 30, 35]
# 	global_flag = True
# 	alphabet = 'ACTG'
# 	diag_score = 10
# 	off_diag_score = 5
# 	dash_score = 0

# 	for idx in range(len(seq_x)):
# 		scoring_matrix = bsm.build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score)
# 		results = compute_alignment_matrix(seq_x[idx], seq_y[idx], scoring_matrix, global_flag)
# 		result = max(max(results))
# 		message = "Test #" + str(idx+1) + ":"
# 		tester.run_test(result, expected[idx], message)

	# compute_alignment_matrix and build_scoring_matrix OWLTEST Troubleshooting
	# [-9.4 pts] compute_alignment_matrix() expected [[0, 0], [0, 6]] but received [[0, -4], [-4, 6]]
	# [-9.4 pts] compute_alignment_matrix('A', 'A', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, False) expected [[0, 0], [0, 6]] but received [[0, -4], [-4, 6]]
	# seq_x = 'A'
	# seq_y = 'A'
	# scoring_matrix = {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 
	#                   'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, 
	#                   '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 
	#                   'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 
	#                   'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}
	# expected = [[0, 0], [0, 6]]
	# tester.run_test(compute_alignment_matrix(seq_x, seq_y, scoring_matrix, False), expected, "OWLTest #5")

	# [-8.8 pts] compute_alignment_matrix() 
	# expected [[0, 0, 0, 0], [0, 6, 2, 2], [0, 2, 8, 4], [0, 2, 4, 14]] 
	# but received [[0, 0, 0, 0], [0, 6, 2, 0], [0, 2, 8, 4], [0, 0, 4, 14]]
	# seq_x = 'ATG'
	# seq_y = 'ACG'
	# scoring_matrix = {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 
	# 				  'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, 
	# 				  '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 
	# 				  'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 
	# 				  'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}
	# expected = [[0, 0, 0, 0], [0, 6, 2, 2], [0, 2, 8, 4], [0, 2, 4, 14]]
	# tester.run_test(compute_alignment_matrix(seq_x, seq_y, scoring_matrix, False), expected, "OWLTest #6")

	# [-4.4 pts] compute_alignment_matrix() 
	# expected [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 1, 0, 0, 0, 0], [0, 0, 2, 1, 1, 4, 3, 2, 1, 0], [0, 0, 1, 4, 3, 3, 6, 5, 4, 3]] 
	# but received [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 1, 0, 0, 0, 0], [0, 0, 1, 0, 1, 4, 3, 2, 1, 0], [0, 0, 0, 3, 2, 3, 6, 5, 4, 3]]
	# compute_alignment_matrix( , False) 
	# seq_x = 'cat'
	# seq_y = 'batcatdog'
	# scoring_matrix = {'-': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'a': {'-': -1, 'a': 2, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'c': {'-': -1, 'a': -1, 'c': 2, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'b': {'-': -1, 'a': -1, 'c': -1, 'b': 2, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'e': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': 2, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'd': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': 2, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'g': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': 2, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'f': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': 2, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'i': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': 2, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'h': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': 2, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'k': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': 2, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'j': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': 2, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'm': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': 2, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'l': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': 2, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'o': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': 2, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'n': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': 2, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'q': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': 2, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'p': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': 2, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 's': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': 2, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'r': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': 2, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'u': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': 2, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 't': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': 2, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'w': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': 2, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'v': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': 2, 'y': -1, 'x': -1, 'z': -1}, 'y': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': 2, 'x': -1, 'z': -1}, 'x': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': 2, 'z': -1}, 'z': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': 2}}
	# expected = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 1, 0, 0, 0, 0], [0, 0, 2, 1, 1, 4, 3, 2, 1, 0], [0, 0, 1, 4, 3, 3, 6, 5, 4, 3]]
	# tester.run_test(compute_alignment_matrix(seq_x, seq_y, scoring_matrix, False), expected, "OWLTest #7")


	# [-19.4 pts] compute_alignment_matrix('A', 'A', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, True) expected [[0, -4], [-4, 6]] but received [[0, -4], [0, 6]]
	# seq_x = 'A'
	# seq_y = 'A'
	# scoring_matrix = {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}
	# expected = [[0, -4], [-4, 6]]
	# tester.run_test(compute_alignment_matrix(seq_x, seq_y, scoring_matrix, True), expected, "OWLTest #8")

	# tester.report_results()
	# print "\n\n"



#####################################################################
# Alignment functions

# For the second part of Project 4, you will use the alignment matrix returned by compute_alignment_matrix to compute global and local alignments of two sequences seq_x and seq_y. The first function will implement the method ComputeAlignment discussed in Question 9 of the Homework.
def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """ Takes as input two sequences seq_x and seq_y whose elements share a common alphabet with the scoring matrix scoring_matrix. This function computes a global alignment of seq_x and seq_y using the global alignment matrix alignment_matrix.The function returns a tuple of the form (score, align_x, align_y) where score is the score of the global alignment align_x and align_y. Note that align_x and align_y should have the same length and may include the padding character '-'. """
    num_rows = len(seq_x)
    num_cols = len(seq_y)
    x_prime = ''
    y_prime = ''

    while num_rows != 0 and num_cols != 0:
        if alignment_matrix[num_rows][num_cols] == alignment_matrix[num_rows-1][num_cols-1] + scoring_matrix[seq_x[num_rows-1]][seq_y[num_cols-1]]:
            x_prime = seq_x[num_rows-1] + x_prime
            y_prime = seq_y[num_cols-1] + y_prime
            num_rows -= 1
            num_cols -= 1
        else:
            if alignment_matrix[num_rows][num_cols] == alignment_matrix[num_rows-1][num_cols] + scoring_matrix[seq_x[num_rows-1]]['-']:
                x_prime = seq_x[num_rows-1] + x_prime
                y_prime = '-' + y_prime
                num_rows -= 1
            else:
                x_prime = '-' + x_prime
                y_prime = seq_y[num_cols-1] + y_prime
                num_cols -= 1
    
    while num_rows != 0:
        x_prime = seq_x[num_rows-1] + x_prime
        y_prime = '-' + y_prime
        num_rows -= 1

    while num_cols != 0:
        x_prime = '-' + x_prime
        y_prime = seq_y[num_cols-1] + y_prime
        num_cols -= 1

    # compute score of alignment
    score = 0
    for position in range(len(x_prime)):
        score += scoring_matrix[x_prime[position]][y_prime[position]]

    return (score, x_prime, y_prime)


# def test_compute_global_alignment():
# 	""" tests compute_global_alignment """
# 	tester = test.TestSuite()
# 	alphabet = 'ACTG'
# 	diag_score = [10, 10, 10, 10, 8, 5]
# 	off_diag_score = [5, 5, 5, 5, -1, -1]
# 	dash_score = [0, 0, 0, 0, -5, -5]
# 	seq_x = ['AC', 'AC', 'ATG', 'CATG', 'CCA', 'CAG']
# 	seq_y = ['T', 'TAC', 'GATG', 'GATG', 'CAC', 'GAC']
# 	global_flag = [True, True, True, True, False, False]
# 	expected = [5, 20, 30, 35, 11, 5]	
# 	results = []
	
# 	for idx in range(len(seq_x)):
# 		scoring_matrix = build_scoring_matrix(alphabet, diag_score[idx], off_diag_score[idx], dash_score[idx])
# 		alignment_matrix = compute_alignment_matrix(seq_x[idx], seq_y[idx], scoring_matrix, global_flag[idx])
# 		global_alignment = compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix)
# 		message = "Test #" + str(idx+1) + ":"
# 		tester.run_test(global_alignment, expected[idx], message)


def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """ Takes as input two sequences seq_x and seq_y whose elements share a common alphabet with the scoring matrix scoring_matrix. This function computes a local alignment of seq_x and seq_y using the local alignment matrix alignment_matrix.The function returns a tuple of the form (score, align_x, align_y) where score is the score of the optimal local alignment align_x and align_y. Note that align_x and align_y should have the same length and may include the padding character '-'. """
    num_rows = len(seq_x)
    num_cols = len(seq_y)
    x_prime = ''
    y_prime = ''

    while num_rows != 0 and num_cols != 0:
        if alignment_matrix[num_rows][num_cols] == alignment_matrix[num_rows-1][num_cols-1] + scoring_matrix[seq_x[num_rows-1]][seq_y[num_cols-1]]:
            x_prime = seq_x[num_rows-1] + x_prime
            y_prime = seq_y[num_cols-1] + y_prime
            num_rows -= 1
            num_cols -= 1
        else:
            if alignment_matrix[num_rows][num_cols] == alignment_matrix[num_rows-1][num_cols] + scoring_matrix[seq_x[num_rows-1]]['-']:
                x_prime = seq_x[num_rows-1] + x_prime
                y_prime = '-' + y_prime
                num_rows -= 1
            else:
                x_prime = '-' + x_prime
                y_prime = seq_y[num_cols-1] + y_prime
                num_cols -= 1

    while num_rows != 0:
        x_prime = seq_x[num_rows-1] + x_prime
        y_prime = '-' + y_prime
        num_rows -= 1

    while num_cols != 0:
        x_prime = '-' + x_prime
        y_prime = seq_y[num_cols-1] + y_prime
        num_cols -= 1

    # compute score of alignment
    score = 0
    for position in range(len(x_prime)):
        score += scoring_matrix[x_prime[position]][y_prime[position]]

    return (score, x_prime, y_prime)
    

# As you implement each matrix function, test it thoroughly. Use the function build_scoring_matrix to generate scoring matrices for alphabets such as "ACTG" and "abcdefghijklmnopqrstuvwxyz". Realistic choices for the scoring matrix should have large scores on the diagonal to reward matching the same character and low scores off the diagonal to penalize mismatches. Use these scoring matrices to test compute_alignment_matrix for simple examples that you can verify by hand. Once you are confident that your implementation of these two functions is correct, submit your code to this Owltest page, which will automatically test your project.

# Next, implement your alignment functions. Use the alignment matrices to generate global and local alignments for simple test examples. Verifying that the global alignments are correct is relatively easy. Generating interesting local alignments and verifying that they are correct is harder. In general, the off-diagonal and dash scores in your scoring matrix should be negative for local alignments. One interesting test for your local alignment function is to choose a scoring matrix that mimics the computation of the longest common subsequence of seq_x and seq_y. Once you are confident that your implementation of these two functions is correct, submit your code to this Owltest page, which will automatically test your project.

# test_compute_global_alignment()