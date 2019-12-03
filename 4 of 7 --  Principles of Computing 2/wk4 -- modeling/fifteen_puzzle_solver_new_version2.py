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

        self.get_zero_pos()
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
        """
        # test assrtion that target_row > 1 and target_col > 0
        assert target_row > 1
        assert target_col > 0

        # find the current position of the tile that should appear at this position in a solved puzzle
        clone = self.clone()
        clone.update_target_tile(target_row, target_col)
        move_string = ""
        temp_string = ''
        clone.get_zero_pos()
        ttile_row = clone.get_target_tile()[0]
        ttile_col = clone.get_target_tile()[1]
        zero_row = clone.get_zero_pos()[0]
        zero_col = clone.get_zero_pos()[1]
        print "move_string:", move_string
        print "temp string:", temp_string  

        if target_col == ttile_col:
            col_multi = 1
        else:
            col_multi = abs(target_col - ttile_col)
        if target_row == ttile_row:
            row_multi = 1
        else:
            row_multi = abs(target_row - ttile_row)    

        # Base case
        if ttile_row == target_row and ttile_col == target_col:
            print "\n*-*-*-*-"
            print "base case ..."
            print clone.__str__()
            return ''

        # Recursive case
        # Our solution strategy will be to move the zero tile up and across 
        # to the target tile.  Then we will move the target tile back to the 
        # target position by applying a series of cyclic moves to the zero tile 
        # that move the target tile back to the target position one position 
        # at a time. Our implementation of this strategy will have three cases 
        # depending on the relative horizontal positions of the zero tile and the 
        # target tile.
        #
        # 3 --> 2 --> 1
        # Case 3:  Move zero tile to same row as target tile
        # Case 2:  Move zero tile to target tile's position in row
        # Case 1:  Cyclically move target tile, one position at a time, to target_row, target_col

        # First move zero tile to target tile's location
        temp_string = 'u'

        # NOTE:  Move one position at a time, recursively
        
        # Case 3:  Target tile is neither in same col nor row as zero tile 
        if zero_row != target_row and zero_col != target_col:
            print "\nCase 3"
            if ttile_row > zero_row:
                print "\nCase 3a"
                temp_string = 'd'
            elif ttile_row < zero_row:
                print "\nCase 3b"
                temp_string = 'u'
        # Case 2:  Target tile is in same row as zero tile
        #  We end case two with zero tile above or below target tile
        elif ttile_row == zero_row:
            print "\nCase 2"
            if ttile_col < zero_col and ttile_row > 0: 
                temp_string = 'l'*row_multi + 'ur'
            elif ttile_col > zero_col and ttile_row > 0:
                temp_string = 'r'*row_multi + 'ul'
            if ttile_col < zero_col and ttile_row == 0:
                temp_string = 'l'*row_multi + 'dr'
            elif ttile_col > zero_col and ttile_row == 0:
                temp_string = 'r'*row_multi + 'dl'

        # Case 1: Target tile is adjacent to zero tile
        else:
            diff = target_row - ttile_row
            print "\nCase 1"
            if diff > 0:
                temp_string += 'lddru'
            elif diff < 0:
                temp_string += 'luurd'
            

        # update move string, puzzle, zero position and target tile position   
        move_string += temp_string 
        print "Updating puzzle ..."
        print "move_string:", move_string
        print "temp string:", temp_string
        clone.update_puzzle(temp_string)
        clone.get_zero_pos()
        clone.update_target_tile(target_row, target_col)
        print clone.__str__()        
        print "//////////////////////////////////////////"
        print "recursive call to clone.solve_interior ..."
        move_string += clone.solve_interior_tile(target_row, target_col)
        print "//////////////////////////////////////////"
        print "move_string:", move_string
        print "\nFinal grid state:"
        print clone.__str__()

        # update the puzzle and return the entire move string
        self.update_puzzle(move_string)
        return move_string

    def get_row_multi(self, target_row, tile_row):
        """ returns distance between target and tile row"""
        if target_row == self.get_target_tile()[0]:
            row_multi = 1
        else:
            row_multi = abs(target_row - self.get_target_tile()[0])
        return row_multi

    def get_col_multi(self, target_col, tile_col):
        """ returns distance between target and tile col"""
        if target_col == self.get_target_tile()[1]:
            col_multi = 1
        else:
            col_multi = abs(target_col - self.get_target_tile()[1])
        return col_multi

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
    print "\n------------------------------------------------------"
    print "Testing solve_interior_tile()\n"
    print "\n------------------------------------------------------"
    print "Test #6:"
    print "Initial grid state:\n"
    initial_grid = [[1, 3, 4], [2, 7, 5], [6, 8, 0], [9, 10, 11]]
    game = Puzzle(4,3,initial_grid)
    print_grid(initial_grid)
    suite.run_test(game.solve_interior_tile(2,2), "l", "Test #6:")

    print "\n------------------------------------------------------"
    print "Test #7:"
    print "Initial grid state:\n"
    initial_grid = [[1, 3, 4], [2, 7, 5], [6, 0, 8], [9, 10, 11]]
    game = Puzzle(4,3,initial_grid)
    print_grid(initial_grid)
    suite.run_test(game.solve_interior_tile(2,1), "u", "Test #7:")

    # should produce an assertion error
    # print "\n------------------------------------------------------"
    # print "Test #8:"
    # print "Initial grid state:\n"
    # initial_grid = [[1, 3, 4], [2, 6, 5], [0, 7, 8], [9, 10, 11]]
    # game = Puzzle(4,3,initial_grid)
    # print_grid(initial_grid)
    # suite.run_test(game.solve_interior_tile(2,0), "assertion error", "Test #8:")

    print "\n------------------------------------------------------"
    print "Test #9:"
    print "Initial grid state:\n"
    initial_grid = [[1, 3, 4], [2, 7, 5], [8, 6, 0], [9, 10, 11]]
    game = Puzzle(4,3,initial_grid)
    print_grid(initial_grid)
    suite.run_test(game.solve_interior_tile(2,2), "llurrdl", "Test #9:") 

    # should produce an assertion error
    # print "\n------------------------------------------------------"
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
    suite.run_test(game.solve_interior_tile(2,2), "uldrul", "Test #11:")

    print "\n------------------------------------------------------"
    print "Test #12:"
    print "Initial grid state:\n"
    initial_grid = [[8, 7, 6], [5, 4, 3], [2, 1, 0]]
    game = Puzzle(3,3,initial_grid)
    print_grid(initial_grid)
    suite.run_test(game.solve_interior_tile(2,2), "uulldrruldrulddruld", "Test #12:")
    # print "returned incorrect move string 'uulldrruld'"
    # NOTE:  target_tile position doesn't appear to be updating correctly    

    # OwlTest results:
    # [-5.0 pts] For obj = Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]]), obj.row0_invariant(0) expected True but received False
    # [-4.8 pts] For obj = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]]), obj.row1_invariant(1) expected True but received False
    # [-8.0 pts] For obj = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]]), obj.solve_2x2() returned incorrect move string ''
    # [-8.0 pts] For obj = Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [0, 7, 8]]), obj.solve_col0_tile(2) returned incorrect move string ''
    # [-8.0 pts] For obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]]), obj.solve_interior_tile(2, 2) returned incorrect move string (Exception: RuntimeError) "maximum recursion depth exceeded" at line 86, in get_zero_pos
    # [-25.0 pts] For obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]]), obj.solve_puzzle() returned incorrect move string ''
    # [-8.0 pts] For obj = Puzzle(3, 3, [[4, 1, 0], [2, 3, 5], [6, 7, 8]]), obj.solve_row0_tile(2) returned incorrect move string ''
    # [-8.0 pts] For obj = Puzzle(3, 3, [[2, 5, 4], [1, 3, 0], [6, 7, 8]]), obj.solve_row1_tile(2) returned incorrect move string ''
    # [-2.0 pts] 1 style warnings found (maximum allowed: 10 style warnings)
    
    suite.report_results()

run_suite()