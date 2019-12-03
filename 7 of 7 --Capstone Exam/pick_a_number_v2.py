# Fundamentals of Computing Capstone Exam
# Question 17

def pick_a_number(board):
	""" recursively takes a list representing the game board and returns a tuple that is the score of the game if both players play optimally by choosing the highest number of the two at the far left and right edge of the number list (board)

	returns a tuple with current player's score first and other player's score second """
	# base case
	print "board:", board
	if len(board) == 2:
		return max(board)
	else:
		pick = max(board[0],board[len(board)-1])
		return [(pick, ), pick_a_number(board)]


def test_pa_num():
	""" tests pick_a_number """
	inputs = [[5,2,3,1]]
	expected = [(3, 8)]
	test_num = 1
	num_failed = 0

	for item in inputs:
		actual = pick_a_number(item)
    	exp = expected[inputs.index(item)]
    	print "\n\n----------------- Test #%r ----------------- \nresult:   %r\nexpected: %r\n" % (test_num, actual, exp)
    	if actual != exp:
    		num_failed += 1
	
	print "\n\n\n-------------- %r test(s) failed. ------------" % num_failed

test_pa_num()