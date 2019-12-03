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
        self._zero_pos = current_position
        return self._zero_pos

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
            return ''

        # Recursive case
        # case 1: target tile is in same col (above zero tile)
        if ttile_col == zero_col:
            if row_multi == 1:          
                temp_string += 'uld'
            elif ttile_row < zero_row and zero_col < clone.get_width() - 1:
                temp_string += 'u' * col_multi + 'r' + 'd' * col_multi + 'lurd'               
            elif ttile_row < zero_row and zero_col == clone.get_width() - 1:
                temp_string += 'u' * row_multi + 'l' + 'dd' + 'ruld'
        # case 2: target tile is in same row (to left or right of zero tile)
        elif ttile_row == zero_row:
            if col_multi == 1 and ttile_row == target_row:
                temp_string += 'l'
            elif ttile_col < zero_col and zero_row < target_row:
                temp_string += 'l' * col_multi + 'd' + 'r' * col_multi + 'uld'
            elif ttile_col < zero_col and zero_row == target_row:
                temp_string += 'l' * col_multi + 'u' + 'r' * col_multi + 'dl'
            elif ttile_col > zero_col and zero_row < target_row and target_col == ttile_col:
                temp_string += 'druld'*abs(ttile_row - target_row)
            elif zero_row > 0:
                temp_string += 'rulld'
            else:
                temp_string += 'rdlulddruld'
        # case 3: neither (1) same col nor (2) same row
        else:
            print clone.__str__()
            if ttile_row > zero_row:
                temp_string += 'd' * abs(ttile_row - zero_row)
            elif ttile_row < zero_row:
                temp_string += 'u' * abs(ttile_row - zero_row)
            elif ttile_row == zero_row and zero_col < self.get_width():
                temp_string += 'druld'

        # update move string, puzzle, zero position and target tile position   
        move_string += temp_string 
        clone.update_puzzle(temp_string)
        clone.get_zero_pos()
        clone.update_target_tile(target_row, target_col)
        move_string += clone.solve_interior_tile(target_row, target_col)

        # update the puzzle and return the entire move string
        self.update_puzzle(move_string)
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert target_row > 1
                
        clone = self.clone()
        clone.update_target_tile(target_row, 0)
        clone.get_zero_pos()
        ttile = clone.current_position(target_row, 0)
        ttile_row = ttile[0]
        ttile_col = ttile[1]
        move_string = ''
        target_col = 0
        zero_row = clone.get_zero_pos()[0]
        zero_col = clone.get_zero_pos()[1]
        temp_string = ''

        # base case
        if ttile[0] == target_row and ttile[1] == 0:
            print "base case reached"
            return ''

        # recursive case
        else: 
            # case 1: target tile is at (i−1,1) and zero tile is at (i-1,0)          
            if ttile[0] == target_row-1 and ttile[1] == 1 and zero_row == ttile[0] and zero_col == (ttile[1]-1):
                print "case 1"
                temp_string += 'ruldrdlurdluurddlu' + 'r' * (clone.get_width()-1)
                print "case 1 temp_string:", temp_string
            # case 2: target tile is above initial zero position
            elif ttile[0] == target_row-1 and ttile[1] == 0:                              
                print "case 2"
                temp_string += 'u' + 'r' * (clone.get_width()-1)
                print "case 2 temp_string:", temp_string
            # case 3: otherwise, move target tile to (i−1,1) and zero to (i−1,0)
            else:
                print "case 3"
                print "case 3 initial temp_string:", temp_string
                if target_col == ttile_col:
                    col_multi = 1
                else:
                    col_multi = abs(target_col - ttile_col)
                if target_row == ttile_row:
                    row_multi = 1
                else:
                    row_multi = abs(target_row - ttile_row)

                if ttile[0] < zero_row:
                    print "case 3a"
                    temp_string += 'u' * row_multi
                elif ttile[1] > (zero_col+1):
                    print "case 3b"
                    temp_string += 'r' * row_multi
                else:
                    print "case 3c"
                    temp_string += 'rulld'
                print " case 3 temp_string:", temp_string
            
        # recursive call
        move_string += temp_string
        print "move_string:", move_string
        print "calling clone.update_puzzle() with string '%s'" % (move_string) 
        clone.update_puzzle(move_string)
        clone.get_zero_pos()
        print clone.__str__()
        print "recursive call:"
        move_string += clone.solve_col0_tile(target_row)
        self.update_puzzle(move_string)
        print "final grid state:"
        print self.__str__()
        return move_string

    #############################################################
    # Phase two methods
    # The invariant row1_invariant(j) should check whether tile zero is at (1,j) and whether all positions either below or to the right of this position are solved. The invariant row0_invariant(j) checks a similar condition, but additionally checks whether position (1,j) is also solved. 

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        assert target_col > 1
        invariant2 = True

        invariant1 = self.get_zero_pos()[0] == 0 and self.get_zero_pos()[1] == target_col

        for row in range(2, self.get_height()):
            for col in range(self.get_width()):
                if self.current_position(row, col) != (row, col):
                    invariant2 = False
        print "invariant2: ", invariant2

        for row in range(0, 2):
            for col in range(target_col, self.get_width()):
                print row, col
                if self.current_position(row, col) != (row, col) and (row, col) != self.get_zero_pos():
                    invariant2 = False

        print "invariant1: %s, invariant2: %s" % (invariant1, invariant2)
        if invariant1 and invariant2:
            return True
        return False

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        assert target_col > 1

        invariant1 = self.get_zero_pos()[0] == 1 and self.get_zero_pos()[1] == target_col
        invariant2 = True 

        for row in range(2, self.get_height()):
            for col in range(0, self.get_width()):
                if self.current_position(row, col) != (row, col):
                    invariant2 = False

        if invariant1 and invariant2:
            return True

        return False

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """                
        clone = self.clone()
        clone.update_target_tile(0, target_col)
        clone.get_zero_pos()
        ttile = clone.current_position(0, target_col)
        ttile_row = ttile[0]
        ttile_col = ttile[1]
        move_string = ''
        zero_row = clone.get_zero_pos()[0]
        zero_col = clone.get_zero_pos()[1]
        temp_string = ''

        # base case
        if ttile[0] == 0 and ttile[1] == target_col:
            return ''

        # recursive case
        # move zero tile from (0,j) to (1,j-1)
        elif zero_row != 1 or zero_col != (target_col-2) or ttile_row != 1 or ttile_col != (target_col-1):
            if zero_row == 0 and zero_col == target_col:
                temp_string += 'ld'
            # move ttile to (1,j-1) and zero to (1,j-2)
            elif ttile_col == zero_col:
                temp_string += 'uld'
            # elif ttile_col < zero_col:
            elif ttile_col < zero_col and zero_row == 1:
                temp_string += 'u' + 'l' * (zero_col - ttile_col)
            elif zero_row == 0 and zero_col == (ttile_col-1) and ttile_row == 0:
                temp_string += 'drruld' * ((target_col-1) - ttile_col)
            elif ttile_col == (target_col-1) and ttile_row == 0:
                temp_string += 'ruld'
        # once zero and ttile are in place, move ttile to final location
        else:
            temp_string += 'urdlurrdluldrruld'
            
        # recursive call
        move_string += temp_string 
        clone.update_puzzle(move_string)
        clone.get_zero_pos()
        move_string += clone.solve_row0_tile(target_col)
        self.update_puzzle(move_string)
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        clone = self.clone()
        clone.update_target_tile(1, target_col)
        move_string = ''
        temp_string = ''
        clone.get_zero_pos()
        ttile_row = clone.get_target_tile()[0]
        ttile_col = clone.get_target_tile()[1]
        zero_row = clone.get_zero_pos()[0]
        zero_col = clone.get_zero_pos()[1]

        if ttile_col == target_col:
            col_multi = 1
        else:
            col_multi = abs(target_col - ttile_col)

        # Base case
        if ttile_row == 1 and ttile_col == target_col:
            print "-----base case reached-----"
            return ''

        # "uldruld"
        print "zero_col - ttile_col:", zero_col - ttile_col

        # Recursive case
        if ttile_row == 0 and zero_row == 1:
            print "case 1a"
            temp_string += 'u'
        if ttile_col == zero_col:
            print "case 1b"
            temp_string += 'ld'
        elif zero_col > ttile_col:
            print "case 2a"
            temp_string += 'l' * col_multi
        elif zero_col - ttile_col < -1:
            print "case 2b"
            temp_string += 'r' *col_multi
        elif ttile_row == 1 and zero_col == ttile_col - 1:
            print "case 3"
            temp_string += 'urrdl' * abs(target_col - ttile_col)
        elif ttile_row == 0 and zero_row == 0 and (abs(zero_col - ttile_col) == 1):
            print "case 4"
            temp_string += 'drul' * col_multi + 'd'
        print "temp_string:", temp_string

         # update move string, puzzle, zero position and target tile position   
        move_string += temp_string
        clone.update_puzzle(temp_string)
        clone.get_zero_pos()
        clone.update_target_tile(1, target_col)
  
        # recursive call
        move_string += clone.solve_row1_tile(target_col)

        # update the puzzle and return the entire move string
        self.update_puzzle(move_string)
        return move_string

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