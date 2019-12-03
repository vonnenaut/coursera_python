import build_scoring_matrix as bsm
import compute_alignment_matrix as cam
import poc_simpletest as test

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


def test_compute_global_alignment():
    tester = test.TestSuite()
    alphabet = 'ACTG'
    idx = 0


    # OWLTEST Test #1
    diag_score = 6
    off_diag_score = 2
    dash_score = -4
    seq_x = ''
    seq_y = ''
    global_flag = True
    expected = (0, '', '')	
    scoring_matrix = bsm.build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score)
    alignment_matrix = cam.compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag)
    global_alignment = compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix)
    message = "Test #" + str(idx+1) + ":"
    tester.run_test(global_alignment, expected, message)


    # OWLTEST Test #2
    diag_score = 6
    off_diag_score = 2
    dash_score = -4
    seq_x = 'A'
    seq_y = 'A'
    global_flag = True
    expected = (6, 'A', 'A')  
    scoring_matrix = bsm.build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score)
    alignment_matrix = cam.compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag)
    global_alignment = compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix)
    message = "Test #" + str(idx+1) + ":"
    tester.run_test(global_alignment, expected, message)
    

    # OWLTEST Test #3
    diag_score = 6
    off_diag_score = 2
    dash_score = -4
    seq_x = 'ATG'
    seq_y = 'ACG'
    global_flag = True
    expected = (14, 'ATG', 'ACG')  
    scoring_matrix = bsm.build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score)
    alignment_matrix = cam.compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag)
    global_alignment = compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix)
    message = "Test #" + str(idx+1) + ":"
    tester.run_test(global_alignment, expected, message)
    # [-17.5 pts] compute_global_alignment('ATG', 'ACG', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, [[0, -4, -8, -12], [-4, 6, 2, -2], [-8, 2, 8, 4], [-12, -2, 4, 14]]) expected ({'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, 14, 'ATG', 'ACG', True) but received (Exception: IndexError) "list index out of range" at line 192, in compute_global_alignment


    tester.report_results()
    

test_compute_global_alignment()