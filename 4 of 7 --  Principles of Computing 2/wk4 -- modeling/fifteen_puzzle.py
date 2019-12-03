"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

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
        # replace with your code
        return False

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

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
        # replace with your code
        return ""

# Start interactive simulation
# initial_grid = [[1, 3, 4], [2, 7, 5], [6, 8, 0], [9, 10, 11]]
# initial_grid = [[8, 1, 2, 3], [4, 7, 5, 10], [9, 6, 0, 11], [12, 13, 14, 15]]
# initial_grid = [[4, 13, 1, 3], [5, 10, 2, 7], [8, 12, 6, 11], [9, 0, 14, 15]]
# initial_grid = [[4, 8, 7, 2], [10, 1, 5, 3], [9, 6, 0, 11], [12, 13, 14, 15]]
# initial_grid = [[7, 5, 1, 9], [2, 4, 3, 8], [0, 9, 10, 11], [12, 13, 14, 15]]
# initial_grid = [[1, 2], [0, 4], [3, 5]]
# initial_grid = [[1, 2],[0, 4],[3, 5]]
# initial_grid = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]]
# rdlurldrlrurrldrullldrrulrdruldluldrurdruldr:
# initial_grid = [[1, 6, 5, 4], [3, 7, 2, 0], [8, 9, 10, 11], [12, 13, 14, 15]]
# initial_grid = [[1, 7, 6, 4], [3, 5, 2, 0], [8, 9, 10, 11], [12, 13, 14, 15]]
# initial_grid = [[1, 6, 2, 4], [3, 5, 0, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
# initial_grid = [[4, 2, 1], [3, 0, 5]]
# initial_grid = [[3, 5, 4, 0], [2, 1, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
# initial_grid = [[0, 2], [3, 1]]
# initial_grid = [[4, 2, 1], [3, 5, 0]]
# initial_grid = [[3, 5, 4, 0], [2, 1, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
# initial_grid = [[4, 1, 7], [2, 6, 5], [3, 0, 8]]
# initial_grid = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]]
# initial_grid = [[1, 6, 5, 4], [3, 7, 2, 0], [8, 9, 10, 11], [12, 13, 14, 15]]
# initial_grid = [[1, 6, 5, 4], [3, 7, 2, 0], [8, 9, 10, 11], [12, 13, 14, 15]]
initial_grid = [[8, 2, 11, 7], [6, 0, 4, 3], [ 9, 5, 1, 10]]
# initial_grid = [[4, 2, 10, 7, 9], [1, 0, 11, 8, 3], [17, 6, 18, 14, 12], [5, 19, 15, 16, 13]]

poc_fifteen_gui.FifteenGUI(Puzzle(3,4, initial_grid))