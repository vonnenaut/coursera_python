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

    for row in range(1,num_rows):
    	for col in range(1,num_cols):
    		dp_table[row][col] = max(dp_table[row-1][col-1]+scoring_matrix[seq_x[row-1]][seq_y[col-1]], dp_table[row-1][col]+scoring_matrix[seq_x[row-1]]['-'], dp_table[row][col-1]+scoring_matrix['-'][seq_y[col-1]])
    		if not global_flag and dp_table[row][col] < 0:
    			dp_table[row][col] = 0

    return dp_table






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

    return (alignment_matrix[-1][-1], x_prime, y_prime)


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
    """ Takes as input two sequences seq_x and seq_y whose elements share a common alphabet with the scoring matrix scoring_matrix. This function computes a local alignment of seq_x and seq_y using the local alignment matrix alignment_matrix.  The function returns a tuple of the form (score, align_x, align_y) where score is the score of the optimal local alignment align_x and align_y. Note that align_x and align_y should have the same length and may include the padding character '-'. 

    In this question, we will focus on modifying ComputeGlobalAlignmentScores to compute a matrix of local alignment scores. Our modification is as follows: Whenever Algorithm ComputeGlobalAlignmentScores (in Question 8) computes a value to assign to S[i,j], if the computed value is negative, the algorithm instead assigns 0 to S[i,j]. The result of this computation is the local alignment matrix for the two sequences. No other modification is done.

    ------------
    So, the score is determined only looking at (global or local) alignment matrix. The differences of compute_global_alignment and compute_local_alignment are
        0. Which alignment matrix is used (global or local)
        1. Which number is the score in the alignment matrix
        2. how to achieve this score

    In compute_local_alignment(),
    (1) is done by searching the maximum score in the matrix.
    As for (2), if you have encountered "0", you need to stop tracing back process and the answer you get at the point is the local alignment (Question 13 in the homework).

    "0" values in the local_alignment_matrix only means that we can ignore this at tracing back process because we can abandon the remaining characters.
    For example, in the above case, "AA" and "AA" is the local alignment. If we don't stop tracing back process, you will see the pair like "-AA" and "TAA" and the score of this pair is less than the "AA" and "AA" pair.

    BTW, your Test #1 has wrong expectation:
    'AC' and 'TC' is the local alignment with score 1+5=6.

    ------------

    As for compute_local_alignment(), if you have understood these conceptual/theoretical facts,

    a. the score of local alignment score is the maximum in the local_alignment_matrix
    b. when you have met "0" in your trace back process, you can exit the function
    c. there is no need to go back to (0, 0) position of local_alignment_matrix

    then, I could explain how to implement.

    1. find the maximum score and x and y indices for this cell in the local_alignment_matrix 
    2. different from compute_global_alignment (in which you have started the bottom right cell),
    you need to start from the cell you have found in (1).
    3-1. tracing back process is almost same as compute_global_alignment(), but you need to "break out"
    when 0 is found
    3-2. different from compute_global_alignment(), we don't need to go back to the (0, 0) position of
    the local_alignment_matrix. So, we don't need while loops of "while num_rows != 0" nor "while num_rows != 0"

    Here is a fixed version of your code. You could see a few differences.
    http://www.codeskulptor.org/#user44_csj78iktovlAvuH.py
    """
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


# def test_compute_local_alignment():
#     """ tests compute_local_alignment according to OWLTest results """
#     # [-7.5 pts] compute_local_alignment() returned incorrect score, expected 13 but received 10
#     tester = test.TestSuite()
#     idx = 0

#     # Test 0
#     alphabet = 'ACTG'
#     seq_x = 'AA'
#     seq_y = 'TAAT'
#     scoring_matrix = build_scoring_matrix(alphabet, 10, 4, -6)
#     print "\nscoring_matrix:", scoring_matrix

#     global_alignment_matrix = compute_alignment_matrix(seq_x, seq_y, scoring_matrix, True)
#     print "\nglobal_alignment_matrix:", global_alignment_matrix

#     local_alignment_matrix = compute_alignment_matrix(seq_x, seq_y, scoring_matrix, False)
#     print "local_alignment_matrix:", local_alignment_matrix

#     global_alignment = compute_global_alignment(seq_x, seq_y, scoring_matrix, global_alignment_matrix)
#     local_alignment = compute_local_alignment(seq_x, seq_y, scoring_matrix, local_alignment_matrix)
#     print "\nglobal alignment:", global_alignment
#     print "\nlocal alignment:", local_alignment
    
#     # Test #1
#     idx += 1
#     alphabet = 'ACTG'
#     diag_score = 5
#     off_diag_score = 1
#     dash_score = -1
#     seq_x = 'AC'
#     seq_y = 'TC'
#     global_flag = False
#     expected = (6, 'AC', 'TG')

#     scoring_matrix = build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score)
#     alignment_matrix = compute_alignment_matrix(seq_x, seq_y, scoring_matrix, False)
#     local_alignment = compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix)
#     message = "Test #" + str(idx) + ":"
#     tester.run_test(local_alignment, expected, message)


#     # Test #2 (OWLTest)
#     idx += 1
#     alphabet = 'abcdefghijklmnopqrstuvwxyz'
#     diag_score = 2
#     off_diag_score = -1
#     dash_score = -1
#     seq_x = 'abddcdeffgh'
#     seq_y = 'aabcddefghij'
#     global_flag = False
#     expected = 13

#     scoring_matrix = build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score)
#     alignment_matrix = compute_alignment_matrix(seq_x, seq_y, scoring_matrix, False)
#     local_alignment = compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix)
#     message = "Test #" + str(idx) + ":"
#     tester.run_test(local_alignment, expected, message)

#     tester.report_results()
    

# As you implement each matrix function, test it thoroughly. Use the function build_scoring_matrix to generate scoring matrices for alphabets such as "ACTG" and "abcdefghijklmnopqrstuvwxyz". Realistic choices for the scoring matrix should have large scores on the diagonal to reward matching the same character and low scores off the diagonal to penalize mismatches. Use these scoring matrices to test compute_alignment_matrix for simple examples that you can verify by hand. Once you are confident that your implementation of these two functions is correct, submit your code to this Owltest page, which will automatically test your project.

# Next, implement your alignment functions. Use the alignment matrices to generate global and local alignments for simple test examples. Verifying that the global alignments are correct is relatively easy. Generating interesting local alignments and verifying that they are correct is harder. In general, the off-diagonal and dash scores in your scoring matrix should be negative for local alignments. One interesting test for your local alignment function is to choose a scoring matrix that mimics the computation of the longest common subsequence of seq_x and seq_y. 


# test_compute_global_alignment()
# test_compute_local_alignment()