"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

NAMES = {2: "provided.PLAYERX",
         3: "provided.PLAYERO",
         4: "provided.DRAW"}

PLAYERX = 2
PLAYERO = 3
DRAW = 4

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    board_copy = board.clone()

    # For Testing:
    print "\n\ncurrent board state:\n", board_copy
    print "player:", NAMES[player]
    print "board_copy.check_win():", board_copy.check_win()
    if board_copy.check_win() != None:
        print "score:", SCORES[board_copy.check_win()]

    # base case:
    if board_copy.check_win() in [PLAYERX, PLAYERO, DRAW]:
        return SCORES[board_copy.check_win()], (-1,-1)

    # recursive case:
    for move in board_copy.get_empty_squares():
        board_copy.move(move[0], move[1], player)
        mm_move(board_copy, provided.switch_player(player))
        if board_copy.check_win() == PLAYERX and player == PLAYERX:
            return SCORES[board_copy.check_win()], move
        elif board_copy.check_win() == PLAYERO:
            return SCORES[board_copy.check_win()], move
        elif board_copy.check_win() == DRAW:
            return SCORES[board_copy.check_win()], move

# def mm_move(board, player):
#     """
#     Make a move on the board.
    
#     Returns a tuple with two elements.  The first element is the score
#     of the given board and the second element is the desired move as a
#     tuple, (row, col).
#     """
#     board_copy = board.clone()
#     current_move = (-1,-1)
#     desired_move = ()
#     current_player = player
#     current_score = -99
#     best_score = -99    

#     # base cases -- game is over and either X or O wins or it's a draw
#     if board_copy.check_win() == provided.PLAYERX:
#         current_score = 1
#         best_score = current_score
#         best_move = current_move
#         return best_score, best_move
#     elif board_copy.check_win() == provided.PLAYERO:
#         current_score = -1
#         return -1, (-1, -1)
#     elif board_copy.check_win() == provided.DRAW:
#         current_score = 0
#         return 0, (-1, -1)
#     # recursive case
#     else:   
#         available_moves = board.get_empty_squares()
#         for move in available_moves:
#             current_move = (move[0], move[1])
#             board_copy.move(move[0], move[1], current_player)
#             current_player = provided.switch_player(player)
#             score, current_move = mm_move(board_copy, current_player)

#     # return tuple with score of given board and desired move
#     print "current board state:\n", board_copy
#     print "player:", NAMES[player]
#     print "desired_move:", desired_move
#     print "score:", score, "\n\n"
#     return score*SCORES[player], desired_move


def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)

# Tests
# print "Setting up an in-game board state:\n"
# test_board = provided.TTTBoard(3)
# test_board.move(0, 0, provided.PLAYERX)
# test_board.move(0, 1, provided.PLAYERO)
# test_board.move(0, 2, provided.PLAYERX)
# test_board.move(1, 0, provided.PLAYERO)
# test_board.move(1, 2, provided.PLAYERX)
# test_board.move(2, 2, provided.PLAYERO)
# print test_board
# print "Testing mm_move:"
# print mm_move(test_board, provided.PLAYERX)

# print "\n\n\n--------------------------\nchanging board configuration."
# print "Setting up an in-game board state:\n"
# test_board = provided.TTTBoard(3)
# test_board.move(0, 0, provided.PLAYERX)
# test_board.move(2, 1, provided.PLAYERO)
# test_board.move(0, 2, provided.PLAYERX)
# test_board.move(0, 1, provided.PLAYERO)
# print test_board
# print "Testing mm_move:"
# print mm_move(test_board, provided.PLAYERX)

# print "\n\n\n--------------------------\nchanging board configuration."
# print "Setting up an in-game board state:\n"
# test_board = provided.TTTBoard(3)
# test_board.move(1, 1, provided.PLAYERX)
# test_board.move(2, 0, provided.PLAYERO)
# test_board.move(2, 1, provided.PLAYERX)
# test_board.move(0, 1, provided.PLAYERO)
# print test_board
# print "Testing mm_move:"
# print mm_move(test_board, provided.PLAYERX)

# print "\n\n\n--------------------------\nchanging board configuration."
# print "Setting up an in-game board state:\n"
# print mm_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO], [provided.PLAYERO, provided.PLAYERX, provided.PLAYERX], [provided.PLAYERO, provided.EMPTY, provided.PLAYERO]]), provided.PLAYERX)

# print "Setting up an in-game board state:\n"
# # expected score 0 but received (-1, (1, 2))
# print mm_move(provided.TTTBoard(3, False, [[provided.EMPTY, provided.EMPTY, provided.PLAYERX], [provided.EMPTY, provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY, provided.EMPTY]]), provided.PLAYERO) 
# print "expected score 0 \nbut received (-1, (1, 2))"