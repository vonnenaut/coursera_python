def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
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
