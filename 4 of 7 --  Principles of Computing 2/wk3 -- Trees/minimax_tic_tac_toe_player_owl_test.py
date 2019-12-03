"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided
# import poc_simpletest

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