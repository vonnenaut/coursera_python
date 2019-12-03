"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided
import poc_simpletest

# poc_ttt_provided TTTBoard Class

# constants:
# EMPTY   (1)
# PLAYERX (2)
# PLAYERO (3)
# DRAW    (4)

# methods:
# switch_player(player)     returns PLAYERO in input PLAYERX and PLAYERX
# on input PLAYERO

# get_dim(self)                 returns the dimension of the board

# square(self, row, col)                    returns one of the three
# constants EMPTY, PLAYERX or PLAYERO that corresponds to contents of the
# board at position

# get_empty_squares(self)       returns list of(row,col) tuples for all
# empty squares

# move(self, row, col, player)  place player on board at position (row,col) player should be either constant PLAYERX or PLAYERO.  Does
# nothing if board square is not empty.

# clone(self)                   returns a copy of the board

# Constants for Monte Carlo simulator
# You may change the values but not their names.
NTRIALS = 15         # Number of trials to run
SCORE_CURRENT = 1.0  # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
# grid representing the scores for each played square
scores_grid = [[]]
STATES = {1: "EMPTY",
          2: "PLAYERX",
          3: "PLAYERO",
          4: "DRAW"}


# Outline:
#
# mc_move --> mc_trial(board, player) --> mc_move() -->
# mc_update_scores(scores, board, player) ==> mc_move() -->
# get_best_move(board, scores) --> mc_move() (returns best move to caller,
# provided.play_game)(?)


def mc_trial(board, player):
    """ plays a game, alternating between players """
    # plays a game starting with the given player by making random moves alternating between players;
    # takes a current board and the next player to move
    # should return when the game is over
    # modified board will contain state of the game
    # doesn't return anything because it updates the board directly

    game_state = board.check_win()
    # print "game_state:", game_state
    # print "player:", player

    # keep playing until the game is over
    while game_state not in [provided.PLAYERX, provided.PLAYERO, provided.DRAW]:
        # retrieve a list of all possible moves (open squares)
        available_moves = board.get_empty_squares()

        # randomly pick an open square to place a move, checking that there are
        # available moves left
        try:
            random_index = random.randrange(0, len(available_moves))

        except ValueError:  # exit the while loop if there are no moves left
            print "No values left in available_moves"
            return

        random_square = available_moves[random_index]
        row = random_square[0]
        col = random_square[1]

        # move to randomly-picked open square
        board.move(row, col, player)
        # switch players
        player = provided.switch_player(player)
        # update the game state
        game_state = board.check_win()
    print "mc_trial(): winner:", STATES[game_state]


def traverse_grid(board, num_steps):
    """ helper method which allows traversal of the game board.
        This method returns the values of the game board in a list. """
    _values_list = [[0 for dummy_col in range(
        num_steps)] for dummy_row in range(num_steps)]

    for row in range(num_steps):
        for col in range(num_steps):
            _values_list[row][col] = board.square(row, col)
    return _values_list


def mc_update_scores(scores, board, player):
    """ scores completed game board, updating scores grid """
    # takes a grid of scores (a list of lists) with same dimensions as TTT board, a board form a completed game and which player the machine player is; scores the completed board and updates the scores grid;
    # does not return anything

    # find out who won
    winner = board.check_win()
    print board.get_dim()
    squares = traverse_grid(board, board.get_dim())
    print "mc_update_scores(): squares:", squares
    # print provided.EMPTY, provided.PLAYERX, provided.PLAYERO, provided.DRAW

    # score appropriately according to winner (or draw state)
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if winner == provided.PLAYERX and squares[row][col] == provided.PLAYERX:
                scores[row][col] += SCORE_CURRENT
            elif winner == provided.PLAYERO and squares[row][col] == provided.PLAYERO:
                scores[row][col] += SCORE_OTHER
    print "mc_update_scores():  scores:", scores

    # if winner == provided.PLAYERX:
    #     for value in values:
    #         if value == provided.PLAYERX:
    #             scores_grid[board.index(value)] += SCORE_CURRENT
    # elif winner == provided.PLAYERO:
    #     for value in values:
    #         if value == provided.PLAYERO:
    #             scores_grid[board.index(value)] += SCORE_OTHER

    # else:       # the game is a draw so don't add anything to the scores grid
    # pass
    print "winner:", winner
    print board
    print "scores:", scores


def get_2d_index(two_dim_list, value, available_moves):
    """ returns the index of a value in a 2d list """
    for row, col in enumerate(two_dim_list):
        if value in col:
            if (row, col.index(value)) in available_moves:
                return (row, col.index(value))
    else:
        print "%r not in %r" % (value, two_dim_list)
        return None


def get_best_move(board, scores):
    """ takes current board and grid of scores; finds all the empty squares with maximum score and randomly returns one of them """
    # returns a (row, column) tuple to mc_move()
    # get all of the available moves/empty squares
    print "\n\nget_best_move(): calculating best move:\n"
    available_moves = board.get_empty_squares()
    print "available_moves:", available_moves
    best_move = None
    choices = [[0 for dummy_col in range(board.get_dim())
                ] for dummy_row in range(board.get_dim())]
    print "scores:", scores

    # given all the open squares' indices (tuples)
    for index in available_moves:
        choices[index[0]][index[1]] = scores[index[0]][
            index[1]]  # take the associated scores

    print "choices:", choices
    max_score = max(choices)
    print "max_score:", max_score
    print "best_move:"
    return best_move


def mc_move(board, player, trials):
    """ uses Monte Carlo simulation to return a move for machine player """
    # returns a tuple as (row, column)
    # (?) calls mc_trial()
    scores_grid = [[0 for dummy_col in range(board.get_dim())
                    ] for dummy_row in range(board.get_dim())]

    trial_num = 1

    # create indices for traversing grid
    # create_initial_indices()

    # set current board to be a copy of the actual game board
    current_board = board.clone()

    # play an entire game on the board randomly choosing moves for number of
    # trials
    while trial_num < trials:
        # run one simulated game trial
        mc_trial(current_board, player)
        # score the resulting board and add it to a running total across all
        # game trials
        mc_update_scores(scores_grid, current_board, player)

    # randomly select an empty square on the board that has the maximum score
    get_best_move(current_board, scores_grid)


# Tests
class run_test_suite():
    """ Testing suite for Tic Tac Toe """

    def __init__(self):
        # create a TestSuite object
        self.suite = poc_simpletest.TestSuite()
        # create a Tic Tac Toe object
        self.board = provided.TTTBoard(3)
        print "Setting up an in-game board state:\n"
        self.board.move(0, 0, provided.PLAYERX)
        self.board.move(1, 1, provided.PLAYERO)
        self.board.move(0, 2, provided.PLAYERX)
        self.board.move(1, 0, provided.PLAYERO)
        print "Actual initial board state:\n", self.board
        print "Cloning board for simulation."
        self.current_board = self.board.clone()
        self.trial = 1
        self.num_trials = NTRIALS
        # initialize scores_grid
        self.scores_grid = [[0 for dummy_col in range(self.current_board.get_dim())
                             ] for dummy_row in range(self.current_board.get_dim())]
        self.run_tests()

    def run_tests(self):
        """ runs specific tests and reports results """
        while self.trial < self.num_trials:
            print "\n------Trial #", self.trial, "------\n"

            # test mc_trial()
            print "Running mc_trial() Test #1:"
            mc_trial(self.current_board, provided.PLAYERX)
            print "run_tests(): current_board:\n", self.current_board
            print "Winner:", STATES[self.current_board.check_win()]

            # test mc_update_scores()
            print "Running mc_update_scores() Test #1:"
            mc_update_scores(self.scores_grid,
                             self.current_board, provided.PLAYERX)
            print "scores_grid:", self.scores_grid
            self.trial += 1

            # # reset current_board and verify scores data is persisting
            self.current_board = self.board.clone()
            print "current_board reset:\n", self.current_board
            print "scores_grid:", self.scores_grid
        print "\n\nCompleted %d simulations." % self.trial

        # print "Setting up an in-game board state:\n"
        # self.current_board.move(0, 0, provided.PLAYERX)
        # self.current_board.move(0, 1, provided.PLAYERO)
        # self.current_board.move(0, 2, provided.PLAYERX)
        # self.current_board.move(1, 0, provided.PLAYERO)
        # print self.current_board

        # test get_best_move()
        print "Running get_best_move() Test #1:"
        print get_best_move(self.current_board, self.scores_grid)

        # # test mc_trial()
        # print "Running mc_trial() Test #1:"
        # mc_trial(self.current_board, provided.PLAYERX)
        # print "current_board:\n", self.current_board
        # print "Winner:", self.current_board.check_win()

        # # test mc_update_scores()
        # print "Running mc_update_scores() Test #1:"
        # mc_update_scores(self.scores_grid,
        #                  self.current_board, provided.PLAYERX)
        # print "scores_grid:", self.scores_grid

        # # test get_best_move()
        # print "Running get_best_move() Test #1:"
        # print get_best_move(self.board, self.scores_grid)

        # # reset current_board
        # self.current_board=self.board.clone()
        # print "current_board reset:", self.current_board

        # # test mc_trial()
        # print "Running mc_trial() Test #2:"
        # mc_trial(self.current_board, provided.PLAYERX)
        # print "current_board:\n", self.current_board
        # print "Winner:", self.current_board.check_win()

        # # test mc_update_scores()
        # print "Running mc_update_scores() Test #2:"
        # mc_update_scores(self.scores_grid, self.current_board, provided.PLAYERX)
        # print "scores_grid:", self.scores_grid

        # # reset current_board
        # self.current_board=self.board.clone()
        # print "current_board reset:", self.current_board

        # # test mc_trial()
        # print "Running mc_trial() Test #3:"
        # mc_trial(self.current_board, provided.PLAYERX)
        # print "current_board:\n", self.current_board
        # print "Winner:", self.current_board.check_win()

        # # test mc_update_scores()
        # print "Running mc_update_scores() Test #3:"
        # mc_update_scores(self.scores_grid, self.current_board, provided.PLAYERX)
        # print "scores_grid:", self.scores_grid

        # # print a report of final test results
        print "\n"
        self.suite.report_results()


# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
test = run_test_suite()
