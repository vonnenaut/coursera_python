import build_scoring_matrix as bsm
import poc_simpletest as test


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
            # print "\n\n------row: %r col: %r------" % (row, col)
            # print "seq_x[row-1]:", seq_x[row-1], "seq_y[col-1]:", seq_y[col-1], "\n"
            # print "dp_table[row-1][col-1]:", dp_table[row-1][col-1]
            # print "scoring_matrix[seq_x[row-1]][seq_y[col-1]]:", scoring_matrix[seq_x[row-1]][seq_y[col-1]]
            # print "dp_table[row-1][col-1]+scoring_matrix[seq_x[row-1]][seq_y[col-1]]:", dp_table[row-1][col-1]+scoring_matrix[seq_x[row-1]][seq_y[col-1]]
            # print "dp_table[row-1][col]:", dp_table[row-1][col]
            # print "scoring_matrix[seq_x[row-1]]['-']:", scoring_matrix[seq_x[row-1]]['-']
            # print "\ndp_table[row-1][col]+scoring_matrix[seq_x[row-1]]['-']:", dp_table[row-1][col]+scoring_matrix[seq_x[row-1]]['-']
            # print "dp_table[row][col-1]:", dp_table[row][col-1]
            # print "scoring_matrix['-'][seq_y[col-1]]:", scoring_matrix['-'][seq_y[col-1]]
            # print "\ndp_table[row][col-1]+scoring_matrix['-'][seq_y[col-1]]:", dp_table[row][col-1]+scoring_matrix['-'][seq_y[col-1]]
            dp_table[row][col] = max(dp_table[row-1][col-1]+scoring_matrix[seq_x[row-1]][seq_y[col-1]], dp_table[row-1][col]+scoring_matrix[seq_x[row-1]]['-'], dp_table[row][col-1]+scoring_matrix['-'][seq_y[col-1]])
            if not global_flag and dp_table[row][col] < 0:
                dp_table[row][col] = 0

    # handle flag -- True = global, False = Local
    # if not global_flag:
    #   for row_idx, row in enumerate(dp_table):
    #       for col_idx, value in enumerate(row):
    #           if value < 0:
    #               dp_table[row_idx][col_idx] = 0
    return dp_table


def test_compute_alignment_matrix():
  """ tests compute_alignment_matrix and uses build_scoring_matrix """
  tester = test.TestSuite()
  seq_x = ['AC', 'AC', 'ATG', 'CATG']
  seq_y = ['T', 'TAC', 'GATG', 'GATG']
  expected = [5, 20, 30, 35]
  global_flag = True
  alphabet = 'ACTG'
  diag_score = 10
  off_diag_score = 5
  dash_score = 0

  for idx in range(len(seq_x)):
      scoring_matrix = bsm.build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score)
      results = compute_alignment_matrix(seq_x[idx], seq_y[idx], scoring_matrix, global_flag)
      result = max(max(results))
      message = "Test #" + str(idx+1) + ":"
      tester.run_test(result, expected[idx], message)

    compute_alignment_matrix and build_scoring_matrix OWLTEST Troubleshooting
    [-9.4 pts] compute_alignment_matrix() expected [[0, 0], [0, 6]] but received [[0, -4], [-4, 6]]
    [-9.4 pts] compute_alignment_matrix('A', 'A', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, False) expected [[0, 0], [0, 6]] but received [[0, -4], [-4, 6]]
    seq_x = 'A'
    seq_y = 'A'
    scoring_matrix = {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 
                      'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, 
                      '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 
                      'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 
                      'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}
    expected = [[0, 0], [0, 6]]
    tester.run_test(compute_alignment_matrix(seq_x, seq_y, scoring_matrix, False), expected, "OWLTest #5")

    [-8.8 pts] compute_alignment_matrix() 
    expected [[0, 0, 0, 0], [0, 6, 2, 2], [0, 2, 8, 4], [0, 2, 4, 14]] 
    but received [[0, 0, 0, 0], [0, 6, 2, 0], [0, 2, 8, 4], [0, 0, 4, 14]]
    seq_x = 'ATG'
    seq_y = 'ACG'
    scoring_matrix = {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 
                    'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, 
                    '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 
                    'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 
                    'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}
    expected = [[0, 0, 0, 0], [0, 6, 2, 2], [0, 2, 8, 4], [0, 2, 4, 14]]
    tester.run_test(compute_alignment_matrix(seq_x, seq_y, scoring_matrix, False), expected, "OWLTest #6")

    [-4.4 pts] compute_alignment_matrix() 
    expected [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 1, 0, 0, 0, 0], [0, 0, 2, 1, 1, 4, 3, 2, 1, 0], [0, 0, 1, 4, 3, 3, 6, 5, 4, 3]] 
    but received [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 1, 0, 0, 0, 0], [0, 0, 1, 0, 1, 4, 3, 2, 1, 0], [0, 0, 0, 3, 2, 3, 6, 5, 4, 3]]
    compute_alignment_matrix( , False) 
    seq_x = 'cat'
    seq_y = 'batcatdog'
    scoring_matrix = {'-': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'a': {'-': -1, 'a': 2, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'c': {'-': -1, 'a': -1, 'c': 2, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'b': {'-': -1, 'a': -1, 'c': -1, 'b': 2, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'e': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': 2, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'd': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': 2, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'g': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': 2, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'f': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': 2, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'i': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': 2, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'h': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': 2, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'k': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': 2, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'j': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': 2, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'm': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': 2, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'l': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': 2, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'o': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': 2, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'n': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': 2, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'q': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': 2, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'p': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': 2, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 's': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': 2, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'r': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': 2, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'u': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': 2, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 't': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': 2, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'w': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': 2, 'v': -1, 'y': -1, 'x': -1, 'z': -1}, 'v': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': 2, 'y': -1, 'x': -1, 'z': -1}, 'y': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': 2, 'x': -1, 'z': -1}, 'x': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': 2, 'z': -1}, 'z': {'-': -1, 'a': -1, 'c': -1, 'b': -1, 'e': -1, 'd': -1, 'g': -1, 'f': -1, 'i': -1, 'h': -1, 'k': -1, 'j': -1, 'm': -1, 'l': -1, 'o': -1, 'n': -1, 'q': -1, 'p': -1, 's': -1, 'r': -1, 'u': -1, 't': -1, 'w': -1, 'v': -1, 'y': -1, 'x': -1, 'z': 2}}
    expected = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 1, 0, 0, 0, 0], [0, 0, 2, 1, 1, 4, 3, 2, 1, 0], [0, 0, 1, 4, 3, 3, 6, 5, 4, 3]]
    tester.run_test(compute_alignment_matrix(seq_x, seq_y, scoring_matrix, False), expected, "OWLTest #7")


    [-19.4 pts] compute_alignment_matrix('A', 'A', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, True) expected [[0, -4], [-4, 6]] but received [[0, -4], [0, 6]]
    seq_x = 'A'
    seq_y = 'A'
    scoring_matrix = {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}
    expected = [[0, -4], [-4, 6]]
    tester.run_test(compute_alignment_matrix(seq_x, seq_y, scoring_matrix, True), expected, "OWLTest #8")

    tester.report_results()
    print "\n\n"

test_compute_alignment_matrix()
 


