# Algorithic Thinking 2
# Week 4 Application 4

# In Project 4, we will implement four functions. The first pair of functions will return matrices that we will use in computing the alignment of two sequences. The second pair of functions will return global and local alignments of two input sequences based on a provided alignment matrix. You will then use these functions in Application 4 to analyze two problems involving comparison of similar sequences.


# Modeling matrices

# For Project 4, you will work with two types of matrices: alignment matrices and scoring matrices. Alignment matrices will follow the same indexing scheme that we used for grids in "Principles of Computing". Entries in the alignment matrix will be indexed by their row and column with these integer indices starting at zero. We will model these matrices as lists of lists in Python and can access a particular entry via an expression of the form alignment_matrix[row][col].

# For scoring matrices, we take a different approach since the rows and the columns of the matrix are indexed by characters in Epsilon in union with '-'. In particular, we will represent a scoring matrix in Python as a dictionary of dictionaries. Given two characters row_char and col_char, we can access the matrix entry corresponding to this pair of characters via scoring_matrix[row_char][col_char].


def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
	""" builds a scoring matrix as a dictionary of dictionaries.

	Takes as input a set of characters alphabet and three scores diag_score, off_diag_score, and dash_score. The function returns a dictionary of dictionaries whose entries are indexed by pairs of characters in alphabet plus '-' 

	One final note for build_scoring_matrix is that, although an alignment with two matching dashes is not allowed, the scoring matrix should still include an entry for two dashes (which will never be used)."""
	alphabet += '-'
	scoring_matrix = {}
	inner_matrix = {}
	# create inner dictionary first
	for letter1 in alphabet:
        for letter2 in alphabet:
            if letter1 == letter2:
                inner_matrix[letter2] = diag_score
    		elif letter1 != letter2 and letter1 != '-' and letter2 != '-':
                inner_matrix[letter2] = off_diag_score
    		elif letter1 == '-' and letter2 == '-':
    			inner_matrix[letter2] = dash_score
    		else:
    			return "Unable to assign value to pair."
    print inner_matrix

    # then assign inner dictionaries to corresponding outer dictionary (letter)

	# initialize matrix's first dimension to dummy value
	# for key in alphabet:
	# 	scoring_matrix[key] = '&'

 #    # populate inner dictionary with second, paired key and corresponding score of that pairing
	# for row_key in scoring_matrix:
	# 	for col_key in alphabet:
	# 		print "row_key:", row_key, "col_key:", col_key
	# 		if row_key == col_key and row_key != '-':
	# 			print "case 1\n\n"
	# 			scoring_matrix[row_key] = {col_key: 10}
	# 		elif row_key and col_key != '-' and row_key != col_key:
	# 			print "case 2\n\n"
	# 			scoring_matrix[row_key]= {col_key: 5}
	# 		else:
	# 			print "case 3\n\n"
	# 			scoring_matrix[row_key]= {col_key: 0}
	# 		print "scoring_matrix:", scoring_matrix
	# print "scoring_matrix[][]:", scoring_matrix['A'] 
	# return scoring_matrix