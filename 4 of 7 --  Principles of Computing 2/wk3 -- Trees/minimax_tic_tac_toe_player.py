"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided
import poc_simpletest

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(90)

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

    # base case:
    if board.check_win() in [PLAYERX, PLAYERO, DRAW]:
        return SCORES[board.check_win()], (-1,-1)
    # recursive case:
    elif player == PLAYERX:
        best_score = -99
        best_move = ()
        for move in board.get_empty_squares():
            board_copy = board.clone()
            board_copy.move(move[0], move[1], player)
            score = mm_move(board_copy, provided.switch_player(player))
            if score[0] > best_score:
                best_move = move
            best_score = max(best_score, score[0])
        return best_score, best_move
    else:
        best_score = 99
        best_move = ()
        for move in board.get_empty_squares():
            board_copy = board.clone()
            board_copy.move(move[0], move[1], player)
            score = mm_move(board_copy, provided.switch_player(player))
            if score[0] < best_score:
                best_move = move
            best_score = min(best_score, score[0])
        return best_score, best_move

    # for move in board_copy.get_empty_squares():
    #     board_copy.move(move[0], move[1], player)
    #     mm_move(board_copy, provided.switch_player(player))
    #     if board_copy.check_win() != None:
    #         print "score:", SCORES[board_copy.check_win()]
    #     if board_copy.check_win() != None:
    #         if board_copy.check_win() == PLAYERX and player == PLAYERX:
    #             return SCORES[board_copy.check_win()], move
    #         elif board_copy.check_win() == PLAYERO and player == PLAYERO:
    #             return SCORES[board_copy.check_win()], move
    #         elif board_copy.check_win() == DRAW:
    #             return SCORES[board_copy.check_win()], move
    #     else:
    #         best_move = mm_move(board_copy, player)
    # return best_move


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
def run_suite():
    """
    Some informal testing code
    """
    
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()

    print "\n------------------------------------------------------"
    print "Initial board state:\n"
    test_board = provided.TTTBoard(3)
    test_board.move(0, 0, provided.PLAYERX)
    test_board.move(1, 0, provided.PLAYERO)
    test_board.move(2, 1, provided.PLAYERX)
    test_board.move(1, 1, provided.PLAYERO)
    print test_board
    print mm_move(test_board, provided.PLAYERX)
    suite.run_test(mm_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.EMPTY, provided.EMPTY], [provided.PLAYERO, provided.PLAYERO, provided.EMPTY], [provided.EMPTY, provided.PLAYERX, provided.EMPTY]]), provided.PLAYERX), (1, (1,2)), "Test #1:")

    # print "\n------------------------------------------------------"   
    # print "Setting up an in-game board state:\n"
    # # expected score 0 but received (-1, (1, 2))
    # print mm_move(provided.TTTBoard(3, False, [[provided.EMPTY, provided.EMPTY, provided.PLAYERX], [provided.EMPTY, provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY, provided.EMPTY]]), provided.PLAYERO) 
    # suite.run_test(mm_move(provided.TTTBoard(3, False, [[provided.EMPTY, provided.EMPTY, provided.PLAYERX], [provided.EMPTY, provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY, provided.EMPTY]]), provided.PLAYERO), (0, ()), "Test #2:")
    # print "expected score 0 \nbut received (-1, (1, 2))"
    
    suite.report_results()

run_suite()

# Owltest output:
# [-25.0 pts] mm_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.EMPTY, provided.EMPTY], [provided.PLAYERO, provided.PLAYERO, provided.EMPTY], [provided.EMPTY, provided.PLAYERX, provided.EMPTY]]), provided.PLAYERX) returned bad move (1, (0, 2))
# [-12.0 pts] mm_move(provided.TTTBoard(3, False, [[provided.EMPTY, provided.EMPTY, provided.PLAYERX], [provided.EMPTY, provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY, provided.EMPTY]]), provided.PLAYERO) expected score 0 but received (-1, (1, 2))