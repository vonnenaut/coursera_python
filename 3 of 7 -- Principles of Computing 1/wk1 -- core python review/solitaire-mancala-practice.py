# solitaire-mancala-practice.py

"""
Student facing implement of solitaire version of Mancala - Tchoukaillon

Goal: Move as many seeds from given houses into the store

In GUI, you make ask computer AI to make move or click to attempt a legal move
"""


class SolitaireMancala:
    """
    Simple class that implements Solitaire Mancala
    """    
    def __init__(self):
        """
        Create Mancala game with empty store and no houses
        """
        # store is left-most list value, house are ascending toward right, opposite of how they are presented visually (left to right descending, store at right-most position).  Below, just the store is created, without any houses yet.
        self.board = [0]
    
    def set_board(self, configuration):
        """
        Take the list configuration of initial number of seeds for given houses
        house zero corresponds to the store and is on right
        houses are number in ascending order from right to left
        """
        self.board = configuration[:]
    
    def __str__(self):
        """
        Return string representation for Mancala board
        """
        str_copy = []

        # reverses order of list for visual representation appropriate to the board's actual layout, with the store on the right
        for dummy_var in self.board:
        	str_copy.insert(0, dummy_var)
        str_copy = str(str_copy)

        return str_copy
    
    def get_num_seeds(self, house_num):
        """
        Return the number of seeds in given house on board
        """
        try:
        	return self.board[house_num]
	    except:
        	return None

    def is_game_won(self):
        """
        Check to see if all houses but house zero are empty
        """
        sum = 0

        for dummy_var in range(1, len(self.board)):
			sum += self.board[dummy_var]
        if sum is 0:
        	return True
        else:
        	return False

    def is_legal_move(self, house_num):
        """
        Check whether a given move is legal
        """
        # if the value of a house number is the same as its index in the list (self.board), then the seed in that positions constitutes a legal move
        if self.board[house_num] is house_num and house_num != 0:
        	return True
        else:
        	return False
    
    def apply_move(self, house_num):
        """
        Move all of the stones from house to lower/left houses
        Last seed must be played in the store (house zero)
        """ 
        for lower_house_num in range(house_num):
        	self.board[lower_house_num] = self.get_num_seeds(lower_house_num) + 1
        if house_num != 0:
        	self.board[house_num] = 0

    def choose_move(self):
        """
        Return the house for the next shortest legal move
        Shortest means legal move from house closest to store
        Note that using a longer legal move would make smaller illegal
        If no legal move, return house zero
        """
        for dummy_var in range(1, len(self.board)):
        	if self.is_legal_move(dummy_var):
        		return dummy_var
        return 0

    def plan_moves(self):
        """
        Return a sequence (list) of legal moves based on the
         following heuristic:
		After each move, move the seeds in the house closest to the store
		when given a choice of legal moves
        Not used in GUI version, only for machine testing
        """
        # Owl test failure troubleshooting
    	# Testing plan_moves() on configuration [0, 1, 2, 3] returned: [1, 2, 3], expected: [1, 2, 1, 3, 1]
        legal_moves = []
        move = -1
        board_sans_store = self.board[1:]

        while any(board_sans_store) and move != 0:
        	move = self.choose_move()
        	legal_moves.append(move)
        	self.apply_move(move)
        return legal_moves

# Create tests to check the correctness of your code

def test_mancala():
    """
    Test code for Solitaire Mancala
    """    
    my_game = SolitaireMancala()
    print "Testing init - Computed:", my_game, "Expected: [0]"
    
    config1 = [0, 0, 1, 1, 3, 5, 0]  
    config2 = [0, 0, 1, 3, 3, 5, 0]
    config3 = [0, 0, 0, 0, 0, 0, 0]
    config4 = [6, 0, 0, 0, 0, 0, 0]
    config5 = [0, 0, 2, 0, 4, 5, 0]
    config6 = [0, 2, 2, 4, 4]
    config7 = [10, 2, 3, 4]
    config8 = [0, 1, 2, 3]

    my_game.set_board(config1)   
    # Test set_board
    print "\nTesting set_board - Computed:", str(my_game), "Expected:", str([0, 5, 3, 1, 1, 0, 0])

    # Test get_num_seeds
    print "\nTesting get_num_seeds - Computed:", my_game.get_num_seeds(1), "Expected:", config1[1]
    print "\nTesting get_num_seeds - Computed:", my_game.get_num_seeds(3), "Expected:", config1[3]
    print "\nTesting get_num_seeds - Computed:", my_game.get_num_seeds(5), "Expected:", config1[5]
    # Test is_legal_move
    print "\nTesting is_legal_move - Computed:", my_game.is_legal_move(5), "Expected:", True
    print "\nesting is_legal_move #2 - Computed:", my_game.is_legal_move(1), "Expected:", False
    print "\nTesting is_legal_move #3 - Computed:", my_game.is_legal_move(3), "Expected:", False
    print "\nTesting is_legal_move #4 - Computed:", my_game.is_legal_move(0), "Expected:", False
    
    # Test apply_move
    print "\nTesting apply_move - Computed:", my_game.apply_move(5), my_game.__str__(), "Expected:", my_game.apply_move(5), [0, 0, 4, 2, 2, 1, 1]
    print "Setting new configuration for next test."
    my_game.set_board(config5)
    print "\nTesting apply_move #2 - Computed:", my_game.apply_move(4), my_game.__str__(), "Expected:", my_game.apply_move(4), [0, 5, 0, 1, 3, 1, 1]

    # Test choose_move
    print "Resetting configuration for next test."
    my_game.set_board(config1)
    print "\nTesting choose_move - Computed:", my_game.choose_move(), "Expected:", 5

    # Test is_game_won
    print "Setting new configuration for next test."
    my_game.set_board(config2)
    print "\nTesting is_game_won - Computed:", my_game.is_game_won(), "Expected:", False
    print "Setting new configuration for next test."
    my_game.set_board(config3)
    print "\nTesting is_game_won #2 - Computed:", my_game.is_game_won(), "Expected:", True
    print "Setting new configuration for next test."
    my_game.set_board(config4)
    print "\nTesting is_game_won #3 - Computed:", my_game.is_game_won(), "Expected:", True
    
    # Test plan_moves
    print "Resetting to original configuration for next test."
    my_game.set_board(config1)
    print "\nTesting plan_moves - Computed:", my_game.plan_moves(), "Expected:", [5]
    print "Changing configuration for next test."
    my_game.set_board(config2)
    print "\nTesting plan_moves #2 - Computed:", my_game.plan_moves(), "Expected:", [3, 5]
    print "Changing configuration for next test."
    my_game.set_board(config3)
    print "\nTesting plan_moves #3 - Computed:", my_game.plan_moves(), "Expected:", []

    print "Changing configuration for next test."
    my_game.set_board(config4)
    print "\nTesting plan_moves #4 - Computed:", my_game.plan_moves(), "Expected:", []
    print "Changing configuration for next test."
    my_game.set_board(config5)
    print "\nTesting plan_moves #5 - Computed:", my_game.plan_moves(), "Expected:", [2, 4, 5]

    # Owl test failure troubleshooting # 1
    print "Resetting configuration for next test."
    my_game.set_board(config6)
    my_game.apply_move(my_game.choose_move())
    print "\nTesting choose_move - Computed:", my_game.board, "Expected:", [1, 3, 0, 4, 4]

    # Owl test failure troubleshooting
    my_game.set_board(config7)
    my_game.apply_move(my_game.choose_move())
    print "\nTesting choose_move - Computed:", my_game.board,"Expected:", [10, 2, 3, 4]

    # Owl test failure troubleshooting
    # Testing plan_moves() on configuration [0, 1, 2, 3] returned: [1, 2, 3], expected: [1, 2, 1, 3, 1]
    my_game.set_board(config8)
    print "\nTesting choose_move - Computed:", my_game.plan_moves(), "Expected:", [1, 2, 1, 3, 1]
   
# test_mancala()


# Import GUI code once you feel your code is correct
# import poc_mancala_gui
# poc_mancala_gui.run_gui(SolitaireMancala())
