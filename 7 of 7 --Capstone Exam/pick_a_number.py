# Fundamentals of Computing Capstone Exam
# Question 17
scores = [0,0]
player = 0


def pick_a_number(board):
	""" recursively takes a list representing the game board and returns a tuple that is the score of the game if both players play optimally by choosing the highest number of the two at the far left and right edge of the number list (board)

	returns a tuple with current player's score first and other player's score second """
	global player
	start = 0
	end = len(board)
	print "board:", board

	# base case
	if len(board) == 1:
		print "\n\n---base case reached---"
		return board
			
	print "\n\n------ recursive case ------"
	print "board:", board
	print "board[0]:", board[0]
	print "board[len(board)-1]:", board[len(board)-1]
	if board[0] >= board[len(board) - 1]:
		print "True"
		choice = board[0]
		start = 1
	else:
		print "False"
		choice = board[len(board)-1]
		end -= 1
	print "board[start:end]:", board[start:end]
	pn_helper(player, choice)
	if player == 0:
		player = 1
	else:
		player = 0
	
	return pick_a_number(board[start:end])
	

def pn_helper(player, value):
	global scores
	scores[player] += value

print "scores:", scores


print pick_a_number([5,2,3,1])
# print pick_a_number([12, 9, 7, 3, 4, 7, 4, 7, 3, 16, 4, 8, 12, 1, 2, 7, 11, 6, 3, 9, 7, 1])