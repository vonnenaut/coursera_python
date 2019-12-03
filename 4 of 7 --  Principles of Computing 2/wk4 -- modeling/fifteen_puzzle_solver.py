"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui
import poc_simpletest

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

        self.set_zero_pos()
        self._target_tile = (0,0)

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    def get_zero_pos(self):
        """
        returns the current position of the zero tile
        """
        for row in range(self.get_height()):
            for col in range(self.get_width()):                    
                if self.get_number(row,col) == 0:
                    current_position = row, col
        return current_position

    def set_zero_pos(self):
        """ sets the zero position on the grid
        """
        self._zero_pos = self.get_zero_pos()

    def get_target_tile(self):
        """ gets target tile position
        """
        return self._target_tile

    def update_target_tile(self, row, col):
        """ updates position of target tile """
        self._target_tile = self.current_position(row, col)

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # Tile zero is positioned at (i,j)
        if self.get_number(target_row,target_col) != 0:
            return False
        # All tiles in rows i+1 or below are positioned at their solved location
        for row in range(target_row+1, self.get_height()):
            for col in range(self.get_width()):
                solved_value = (self.get_width() * row + col)
                if self.get_number(row,col) != solved_value:
                    return False
        # All tiles in row i to the right of position (i,j) are positioned at their solved location
        for col in range(target_col+1, self.get_width()):
            solved_value = (self.get_width() * target_row + col)
            if self.get_number(target_row, col) != solved_value:
                return False
        return True


    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position        
        Updates puzzle and returns a move string

        Implementing solve_interior_tile
        We are now ready to formulate the basic algorithm for solve_interior_tile(i, j). Given a target position (i,j), we start by finding the current position of the tile that should appear at this position in a solved puzzle. We refer to this tile as the target tile.

        While moving the target tile to the target position, we can leverage the fact that lower_row_invariant(i, j) is true prior to execution of solve_interior_tile(i, j). First, we know that the zero tile is positioned at (i,j). Also, the target tile's current position (k,l) must be either above the target position (k<i) or on the same row to the left (i=k and l<j).

        Our solution strategy will be to move the zero tile up and across to the target tile. Then we will move the target tile back to the target position by applying a series of cyclic moves to the zero tile that move the target tile back to the target position one position at a time. Our implementation of this strategy will have three cases depending on the relative horizontal positions of the zero tile and the target tile.


        As per homework problem 8, the strategy will have three cases. One is if target tile is above the zero tile (same column) or target tile to left of zero tile (same row). I got cyclic order for these two. But how to consider scenarios where target tile is not in same row or column as of zero tile.

        Yoshimi KurumaMentor
        Hi. In case target tile is not in the same row or column, you can move zero tile and adjust to match your cases. 
        In solve_interior_tile(), we move zero to the current position of the target without cyclic move (the move in the left image to the middle image in Q8).
        then we use some cyclic things for moving zero and the target tiles together (the moves in the middle image to the right image in Q8).
        For (1), if the row or column is the same, the move in (1) is simpler like 'uuu' or 'lll' (not 'uul' or ull'). But this would not so important.

        The phase one is most difficult part of this mini-project. If you succeed to implement phase one, phase two is not difficult and phase three is easy.

        # OwlTest:  Too many branches (15/12); Too many statements (71/50)
        """
        # test assrtion that target_row > 1 and target_col > 0
        assert target_row > 1
        assert target_col > 0

        # find the current position of the tile that should appear at this position in a solved puzzle
        clone = self.clone()
        clone.update_target_tile(target_row, target_col)
        move_string = ""
        temp_string = ''
        clone.set_zero_pos()
        ttile_row = clone.get_target_tile()[0]
        ttile_col = clone.get_target_tile()[1]
        zero_row = clone.get_zero_pos()[0]
        zero_col = clone.get_zero_pos()[1]
        print "target_row, target_col:", target_row, ",", target_col
        print "target tile pos:", clone.get_target_tile()
        print "_zero_pos:", clone.get_zero_pos()
        print "move_string:", move_string
        print "temp string:", temp_string       

        # base case
        if ttile_row == target_row and ttile_col == target_col:
            print "\nbase case ..."
            return ''

        # recursive case
        if target_col == clone.get_target_tile()[1]:
            col_multi = 1
        else:
            col_multi = abs(target_col - clone.get_target_tile()[1])
        if target_row == clone.get_target_tile()[0]:
            row_multi = 1
        else:
            row_multi = abs(target_row - clone.get_target_tile()[0])          

        # 3 cases:
        # Our solution strategy will be to move the zero tile up and across to the target tile. 
        # Then we will move the target tile back to the target position by applying a series of 
        # cyclic moves to the zero tile that move the target tile back to the target position one
        # position at a time. Our implementation of this strategy will have three cases depending 
        # on the relative horizontal positions of the zero tile and the target tile.

        # case 1: target tile is above zero tile
        if ttile_col == zero_col:
            # move zero tile to target tile position without using cycling movement
            if row_multi == 1:
                print "\nCase 1a"               
                temp_string += 'uld'
            elif ttile_row < zero_row and zero_col < clone.get_width() - 1:
                print "\nCase 1b"
                temp_string += 'u' * col_multi + 'r' + 'd' * col_multi + 'lurd'               
            elif ttile_row < zero_row and zero_col == clone.get_width() - 1:
                print "\nCase 1c"
                temp_string += 'u' * abs(zero_row - ttile_row) + 'l' + 'd' * (abs(zero_row - ttile_row) + 1) + 'ruld'
        # case 2: target tile is in same row as zero tile
        elif ttile_row == zero_row:
            if col_multi == 1 and ttile_row == target_row:
                print "\nCase 2a"
                temp_string += 'l'
            elif ttile_col < zero_col and zero_row < target_row:
                print "\nCase 2b"
                temp_string += 'l' * col_multi + 'd' + 'r' * col_multi + 'uld'
            elif ttile_col < zero_col and zero_row == target_row:
                print "\nCase 2c:"
                temp_string += 'l' * col_multi + 'u' + 'r' * col_multi + 'dl'
        # case 3: neither case 1 nor case 2
        else:
            print "\nCase 3"
            # move zero tile to establish case 1
            if ttile_row < zero_row:
                temp_string += 'u' * row_multi
            elif ttile_row > zero_row:
                temp_string += 'd' * row_multi
            if ttile_col < zero_col:
                temp_string += 'l' * col_multi
            elif ttile_col > zero_col:
                temp_string += 'r' * col_multi
        # update move string, puzzle, zero position and target tile position   
        move_string += temp_string   
        print "Updating puzzle ..."
        print "move_string:", move_string
        print "temp string:", temp_string
        clone.update_puzzle(temp_string)
        clone.set_zero_pos()
        clone.update_target_tile(target_row, target_col)
        print "zero pos:", clone.get_zero_pos()
        print "target tile pos:", clone.get_target_tile()
        print clone.__str__()        
        print "//////////////////////////////////////////"
        print "recursive call to clone.solve_interior ..."
        clone.update_puzzle(clone.solve_interior_tile(target_row, target_col))
        print "//////////////////////////////////////////"
        print "move_string:", move_string
        print clone.__str__()        
        print "target_row, target_col:", target_row, ",", target_col
        print "target tile pos:", clone.get_target_tile()
        # move_string: uulldrruld

        # update the puzzle
        # self.update_puzzle(move_string)
        # self.set_zero_pos()
        # self.get_target_tile()
        # print "self._zero_pos:", self.get_zero_pos()
        # print self.__str__()
        # finally, return the entire move string
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        return False

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        return False

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # assert my_puzzle.lower_row_invariant(i,j)
        # my_puzzle.solve_interior_tile(i, j)
        # assert my_puzzle.lower_row_invariant(i, j - 1)
        return ""


# Start interactive simulation
# poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))


# Tests
def print_grid(grid):
    for row in grid:
        print row
    print "\n"

def run_suite():
    """
    Some informal testing code
    """
    
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()

    # Run a series of tests on lower_row_invariant()
    # print "\n------------------------------------------------------"
    # print "Testing lower_row_invariant()\n"
    # print "\n------------------------------------------------------"
    # print "Test #1:"
    # # print "Initial grid state:\n"
    # initial_grid = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]]
    # game = Puzzle(4,3,initial_grid)
    # # print_grid(initial_grid)
    # suite.run_test(game.lower_row_invariant(0,0), True, "Test #1:")

    # print "\n------------------------------------------------------"
    # print "Test #2:"
    # # print "Initial grid state:\n"
    # initial_grid = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]]
    # game = Puzzle(4,3,initial_grid)
    # # print_grid(initial_grid)
    # suite.run_test(game.lower_row_invariant(1,1), False, "Test #2:")

    # print "\n------------------------------------------------------"
    # print "Test #3:"
    # # print "Initial grid state:\n"
    # initial_grid = [[0, 1, 2], [3, 0, 5], [6, 7, 8], [9, 10, 11]]
    # game = Puzzle(4,3,initial_grid)
    # # print_grid(initial_grid)
    # suite.run_test(game.lower_row_invariant(1,1), True, "Test #3:")

    # print "\n------------------------------------------------------"
    # print "Test #4:"
    # # print "Initial grid state:\n"
    # initial_grid = [[4, 1, 2], [3, 0, 5], [6, 8, 10], [9, 7, 11]]
    # game = Puzzle(4,3,initial_grid)
    # # print_grid(initial_grid)
    # suite.run_test(game.lower_row_invariant(1,1), False, "Test #4:")

    # # print "\n------------------------------------------------------"
    # print "Test #5:"
    # # print "Initial grid state:\n"
    # initial_grid = [[11, 1, 2], [3, 4, 5], [6, 8, 10], [9, 7, 0]]
    # game = Puzzle(4,3,initial_grid)
    # # print_grid(initial_grid)
    # suite.run_test(game.lower_row_invariant(3,2), True, "Test #5:")


    # run a series of tests on solve_interior_tile()
    # print "\n------------------------------------------------------"
    # print "Testing solve_interior_tile()\n"
    # print "\n------------------------------------------------------"
    # print "Test #6:"
    # print "Initial grid state:\n"
    # initial_grid = [[1, 3, 4], [2, 7, 5], [6, 8, 0], [9, 10, 11]]
    # game = Puzzle(4,3,initial_grid)
    # print_grid(initial_grid)
    # suite.run_test(game.solve_interior_tile(2,2), "l", "Test #6:")

    # print "\n------------------------------------------------------"
    # print "Test #7:"
    # print "Initial grid state:\n"
    # initial_grid = [[1, 3, 4], [2, 7, 5], [6, 0, 8], [9, 10, 11]]
    # game = Puzzle(4,3,initial_grid)
    # print_grid(initial_grid)
    # suite.run_test(game.solve_interior_tile(2,1), "uld", "Test #7:")

    # should produce an assertion error
    # print "\n------------------------------------------------------"
    # print "Test #8:"
    # print "Initial grid state:\n"
    # initial_grid = [[1, 3, 4], [2, 6, 5], [0, 7, 8], [9, 10, 11]]
    # game = Puzzle(4,3,initial_grid)
    # print_grid(initial_grid)
    # suite.run_test(game.solve_interior_tile(2,0), "assertion error", "Test #8:")

    # print "\n------------------------------------------------------"
    # print "Test #9:"
    # print "Initial grid state:\n"
    # initial_grid = [[1, 3, 4], [2, 7, 5], [8, 6, 0], [9, 10, 11]]
    # game = Puzzle(4,3,initial_grid)
    # print_grid(initial_grid)
    # suite.run_test(game.solve_interior_tile(2,2), "llurrdl", "Test #9:") 

    # # should produce an assertion error
    # # print "\n------------------------------------------------------"
    # print "Test #10:"
    # print "Initial grid state:\n"
    # initial_grid = [[1, 3, 2], [0, 4, 5], [6, 7, 8], [9, 10, 11]]
    # game = Puzzle(4,3,initial_grid)
    # print_grid(initial_grid)
    # suite.run_test(game.solve_interior_tile(1,0), "u", "Test #10:")

    print "\n------------------------------------------------------"
    print "Test #11:"
    print "Initial grid state:\n"
    initial_grid = [[1, 3, 4], [2, 8, 5], [7, 6, 0], [9, 10, 11]]
    game = Puzzle(4,3,initial_grid)
    print_grid(initial_grid)
    suite.run_test(game.solve_interior_tile(2,2), "uldruld", "Test #11:")

    # print "\n------------------------------------------------------"
    # print "Test #12:"
    # print "Initial grid state:\n"
    # initial_grid = [[8, 7, 6], [5, 4, 3], [2, 1, 0]]
    # game = Puzzle(3,3,initial_grid)
    # print_grid(initial_grid)
    # suite.run_test(game.solve_interior_tile(2,2), "uulldrruldrulddruld", "Test #12:")
    # print "returned incorrect move string 'uulldrruld'"
    # NOTE:  target_tile position doesn't appear to be updating correctly

    

    # OwlTest results:
# [-5.0 pts] For obj = Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]]), obj.row0_invariant(0) expected True but received False
# [-4.8 pts] For obj = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]]), obj.row1_invariant(1) expected True but received False
# [-8.0 pts] For obj = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]]), obj.solve_2x2() returned incorrect move string ''
# [-8.0 pts] For obj = Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [0, 7, 8]]), obj.solve_col0_tile(2) returned incorrect move string ''
# [-8.0 pts] For obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]]), obj.solve_interior_tile(2, 2) returned incorrect move string 'uulldrruld'
# [-25.0 pts] For obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]]), obj.solve_puzzle() returned incorrect move string ''
# [-8.0 pts] For obj = Puzzle(3, 3, [[4, 1, 0], [2, 3, 5], [6, 7, 8]]), obj.solve_row0_tile(2) returned incorrect move string ''
# [-8.0 pts] For obj = Puzzle(3, 3, [[2, 5, 4], [1, 3, 0], [6, 7, 8]]), obj.solve_row1_tile(2) returned incorrect move string ''
# [-6.0 pts] 3 style warnings found (maximum allowed: 10 style warnings)

# [line 178] Too many branches (15/12)
#     function "Puzzle.solve_interior_tile", line 178
# [line 178] Too many statements (71/50)
#     function "Puzzle.solve_interior_tile", line 178


    
    suite.report_results()

run_suite()