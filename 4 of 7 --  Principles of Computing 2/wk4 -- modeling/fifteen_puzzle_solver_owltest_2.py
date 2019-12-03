"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""
# import poc_fifteen_gui

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

    def move_zero_to_lower_right(self):
        """ moves zero tile to pass lower_row_invariant test at beginning of phase one in solve_puzzle
        updates puzzle and returns a move string
        """
        move_string = ''
        zero_row = self.get_zero_pos()[0]
        zero_col = self.get_zero_pos()[1]
        row_multi = (self.get_height()-1) - zero_row
        col_multi = (self.get_width()-1) - zero_col

        if zero_row == self.get_height()-1 and zero_col == self.get_width()-1:
            return ''
        else:
            if row_multi > 0:
                move_string += 'd' * row_multi
            elif row_multi < 0:
                move_string += 'u' * row_multi
            if col_multi > 0:
                move_string += 'r' * col_multi
            elif col_multi < 0:
                move_string += 'l' * col_multi
        # update puzzle and return move string
        print "moving zero tile to lower-right corner of puzzle ..."  
        self.update_puzzle(move_string)              
        print self.__str__()
        return move_string


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

        print "ttile_col, zero_col+1:", ttile_col, zero_col+1  

        # Base case
        if ttile_row == target_row and ttile_col == target_col:
            # if ttile is at (target_row,target_col), move zero tile to next tttile
            if zero_col != target_col-1:
                temp_string += 'l'
            if zero_row != target_row:
                temp_string += 'd'
            return temp_string

        # Recursive case
        # case 1: target tile is in same col as zero
        if ttile_col == zero_col:
            # ttile is above zero tile
            if ttile_row < zero_row:
                print "1a"
                temp_string += 'u' * (zero_row - ttile_row)
            elif ttile_row > zero_row:
                print "1b"
                temp_string += 'ld'

        # case 2: target tile is in same row
        elif ttile_row == zero_row:
            # ttile is to left of zero
            if ttile_col < zero_col:
                print "2a"
                temp_string += 'l' * (zero_col - ttile_col)
            # ttile is more than one position to right of zero
            elif ttile_col > (zero_col+1):
                print "2b"
                temp_string += 'r' * (ttile_col - zero_col)
            # ttile is immediately to right of zero
            elif ttile_col == (zero_col+1):
                # move ttile down to target_row (if ttile is at or left of target_col)
                if ttile_row < target_row and ttile_col <= target_col:
                    print "2c"
                    temp_string += 'drul' + 'ddrul' * (target_row-ttile_row-1) 
                # move ttile left and then down to target_row so as to not disturb already-solved tiles (if zero and ttile row > 0)
                elif ttile_row < target_row and ttile_col > target_col and zero_row > 0:
                    temp_string += 'rulld'
                # for if zero and ttile row is at top
                elif ttile_row < target_row and ttile_col > target_col and zero_row == 0:
                    temp_string += 'rdllu'
                # move ttile to target_col
                elif ttile_row == target_row and ttile_col < target_col:
                    temp_string += 'urrdl' * (target_col-ttile_col)

        # case 3: neither (1) same col nor (2) same row
        else:
            print "Case 3 ..."
            print clone.__str__()
            # ttile is below zero
            if ttile_row > zero_row:
                print "\nCase 3a"
                temp_string += 'd' * abs(ttile_row - zero_row)
            # ttile is above zero
            elif ttile_row < zero_row:
                print "\nCase 3b"
                temp_string += 'u' * abs(ttile_row - zero_row)

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

        # update the puzzle and return the entire move string
        self.update_puzzle(move_string)
        print "\nFinal grid state:"
        print self.__str__()
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
        zero_row = clone.get_zero_pos()[0]
        zero_col = clone.get_zero_pos()[1]
        temp_string = ''

        # base case
        if ttile_row == target_row and ttile_col == 0:
            # if ttile is at (i,0), move zero to right end of row
            if zero_col != clone.get_width()-1:
                temp_string += 'r' * ((clone.get_width()-1)-zero_col)
            print "---base case reached---"
            return temp_string

        # recursive case
        else: 
            # move zero tile from (i,0) to (i-1,1)
            if zero_row == target_row and zero_col == 0:
                print "---//-|| 1 ||-//---"
                temp_string += 'ur'
            # otherwise, move ttile to (i-1,1) and zero to (i-1,0)
            else:
                # ttile is somewhere above i-1 row
                if ttile_row < zero_row:
                    print "---//-|| 2 ||-//---"
                    temp_string += 'u' * (zero_row - ttile_row)
                # ttile is immediately left of zero in same row (i-1) in 0 col
                elif ttile_col == zero_col-1 and ttile_row == zero_row and ttile_row == target_row-1 and ttile_col < 1:
                    print "3"
                    temp_string += 'l'
                # ttile is immediately left of zero above row i-1
                elif ttile_col == zero_col-1 and ttile_row == zero_row and ttile_row < target_row-1:
                    print "---//-|| 4 ||-//---"
                    temp_string += 'dlurd' * ((target_row-1)-ttile_row)
                # ttile is immediately left of zero in row i-1, col > 1
                elif ttile_col == zero_col-1 and ttile_row == target_row-1 and ttile_col > 1:
                    temp_string += 'ulldr' * (ttile_col-2) + 'ulld'
                # ttile is more than one tile to the right of zero
                elif ttile_col > zero_col+1:
                    print "5"
                    temp_string += 'r' * (ttile_col-1)
                # ttile is directly below zero, above i-1 row
                elif ttile_col == zero_col and ttile_row < target_row-1:
                    print "6"
                    temp_string += 'lddru' * ((target_row-1) - ttile_row)
                # ttile is directly below zero, in i-1 row
                elif ttile_row == zero_row + 1 and ttile_col == zero_col and ttile_col == 1:
                    print "7"
                    temp_string += 'ld'  
                # ttile is immediately right of zero in same row above i-1 to right of 1 col
                elif ttile_col == zero_col+1 and ttile_row == zero_row and ttile_row < target_row-1:
                    print "---//-|| 8 ||-//---"
                    temp_string += 'druld' * (target_row-1-ttile_row)
                # ttile is immediately left of zero in same row i-1 to right of 1 col
                # move ttile to left and zero to its left
                elif ttile_col == zero_col+1 and ttile_row == zero_row and ttile_row == target_row-1 and ttile_col > 1:
                    print "---//-|| 9 ||-//---"
                    temp_string += 'rulld' * (ttile_col-1)
                # ttile is immediately right of zero in i-1 row (zero is in same row)
                elif ttile_row == target_row-1 and ttile_row == zero_row and ttile_col == zero_col+1 and ttile_col == 1:
                    print "---//-|| 10 ||-//---"
                    temp_string += 'ruldrdlurdluurddlu' + 'r' * ((clone.get_width()-1)-zero_col)        
            
        # recursive call
        move_string += temp_string
        print "move_string:", move_string
        print "Updating puzzle with string '%s'" % (move_string) 
        clone.update_puzzle(move_string)
        clone.get_zero_pos()
        clone.update_target_tile(target_row, 0)
        print clone.__str__()
        print "///// recursive call /////"
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
        invariant2 = True

        # check whether zero is at (0,j) 
        invariant1 = self.get_zero_pos()[0] == 0 and self.get_zero_pos()[1] == target_col

        # check whether all positions either below or to the right of this position are solved and whether position (1,j) is also solved
        for row in range(2, self.get_height()):
            for col in range(self.get_width()):
                if self.current_position(row, col) != (row, col):
                    invariant2 = False

        for row in range(0, 2):
            for col in range(target_col, self.get_width()):
                if self.current_position(row, col) != (row, col) and (row, col) != self.get_zero_pos():
                    invariant2 = False

        # print "invariant1: %s, invariant2: %s" % (invariant1, invariant2)
        if invariant1 and invariant2:
            return True
        return False

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # check whether zero is at (1,j)
        invariant1 = self.get_zero_pos()[0] == 1 and self.get_zero_pos()[1] == target_col
        invariant2 = True

        # check whether all positions either below or to the right of this position are solved.
        for col in range(target_col+1, self.get_width()):
            if self.current_position(1, col) != (1, col):
                invariant2 = False

        if self.get_height() > 2:
            for row in range(2, self.get_height()):
                for col in range(0, self.get_width()):
                    if self.current_position(row, col) != (row, col):
                        invariant2 = False

        # print "invariant1, invariant 2:", invariant1, invariant2

        if invariant1 and invariant2:
            return True

        return False

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """    
        # assert ?           
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
            # print "case 1"
            return ''

        # recursive case
        # move zero tile from (0,j) to (1,j-1)
        elif zero_row != 1 or zero_col != (target_col-2) or ttile_row != 1 or ttile_col != (target_col-1):
            if zero_row == 0 and zero_col == target_col:
                # print "case 2a"
                temp_string += 'ld'
            # move ttile to (1,j-1) and zero to (1,j-2) (NOTE needs modified for #54):
            elif ttile_col == zero_col-1 and ttile_row == zero_row -1 and ttile_col == clone.get_width()-3:
                # print "case 2b"
                temp_string += 'uldruld'
            # ttile is in row above zero, directly above or to the left
            elif ttile_row == zero_row-1 and (ttile_col == zero_col or ttile_col < zero_col):
                # print "case 2c"
                temp_string += 'uld' + 'uld' * ((zero_col - ttile_col)-1)
            # ttile is left of j-1 and right of zero (same row or above)
            elif ttile_col < target_col-1 and zero_col < ttile_col:
                if ttile_row < zero_row:
                    # print "case 2d1"
                    temp_string += 'rurdl' + 'urrdl' * ((target_col-1)-ttile_col-1)
                else:
                    # print "case 2d2"
                    temp_string += 'urrdl' * ((target_col-1)-ttile_col)
            elif zero_row == 0 and zero_col == (ttile_col-1) and ttile_row == 0:
                # print "case 2e"
                temp_string += 'dr'
            elif ttile_col == target_col-2 and ttile_row == 1 and zero_col == ttile_col-1 and zero_row == 1:
                # print "case 2f"
                temp_string += 'urrdl'
            elif ttile_col < zero_col and ttile_row == zero_row and ttile_row == 1:
                # print "case 2g"
                temp_string += 'l' * (zero_col - ttile_col)
            # print "temp_string", temp_string, "\n"
        # once zero and ttile are in place, move ttile to final location
        else:
            # print "case 3"
            temp_string += 'urdlurrdluldrruld'
            
        # recursive call
        move_string += temp_string 
        clone.update_puzzle(move_string)
        clone.get_zero_pos()
        clone.update_target_tile(0, target_col)
        # print self.__str__()
        # print "\nRecursive call //////////"
        move_string += clone.solve_row0_tile(target_col)
        self.update_puzzle(move_string)
        # print "final grid state:"
        # print self.__str__()
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
            # print "-----base case reached-----"
            return ''

        # print "zero_col - ttile_col:", zero_col - ttile_col

        # Recursive case
        if ttile_row == 0 and zero_row == 1:
            # print "case 1a"
            temp_string += 'u'
        # if ttile_col == zero_col:
        #     print "case 1b"
        #     temp_string += 'ld'
        elif zero_col > ttile_col:
            # print "case 2a"
            temp_string += 'l' * col_multi
        elif zero_col - ttile_col < -1:
            # print "case 2b"
            temp_string += 'r' *col_multi
        elif ttile_row == 1 and zero_col == ttile_col - 1:
            # print "case 3"
            temp_string += 'urrdl' * abs(target_col - ttile_col)
        # elif ttile_col < target_col and zero_col == ttile_col - 1:
        elif ttile_row == 0 and zero_row == 0 and (abs(zero_col - ttile_col) == 1):
            # print "case 4"
            temp_string += 'drul' * col_multi + 'd'
        # print "temp_string:", temp_string

         # update move string, puzzle, zero position and target tile position   
        move_string += temp_string
        clone.update_puzzle(temp_string)
        # print clone.__str__()
        clone.get_zero_pos()
        clone.update_target_tile(1, target_col)
        # print "move_string:", move_string

        # recursive call
        # print "///// recursive call /////"
        move_string += clone.solve_row1_tile(target_col)

        # park zero tile in position for solve_row0
        if clone.get_zero_pos()[0] != 0 and clone.get_zero_pos()[1] != target_col:
            move_string += 'ur'

        # update the puzzle and return the entire move string
        self.update_puzzle(move_string)
        # print self.__str__()
        # print "move_string:", move_string
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        clone = self.clone()
        move_string = ''
        temp_string = ''
        zero_pos = clone.get_zero_pos()
        finished = True

        # base case
        for row in range(2):
            for col in range(2):
                if clone.current_position(row, col) != (row, col):
                    finished = False

        if finished == True:
            return ''

        # recursive case
        if zero_pos[0] != 0:
            temp_string += 'u'
        if zero_pos[1] != 0:
            temp_string += 'l'
        else:
            temp_string += 'rdlu'
        clone.update_puzzle(temp_string)
        clone.get_zero_pos()
        move_string += temp_string

        # recursive call
        move_string += clone.solve_2x2()

        # update puzzle and return move string
        self.update_puzzle(move_string)
        print "2x2 move_string:", move_string
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_string = ''

        print "\nPhase 1 ///////////////"
        # First, solve bottom i-2 rows, bottom to top
        if self.get_height() > 2 or self.get_width() > 2:
            # put zero tile in lower-right corner of puzzle if it's bigger than 2x2
            move_string += self.move_zero_to_lower_right()
            print self.__str__()

        for row in range(self.get_height()-1, 1, -1):
            for col in range(self.get_width()-1, -1, -1):
                # print "row, col:", row, col
                if col > 0:                    
                    assert self.lower_row_invariant(row,col), "lower_row_invariant assertion for %d,%dfailed!" % (row, col)
                    print "\nCalling solve_interior_tile():"
                    move_string += self.solve_interior_tile(row,col)
                    print self.__str__() 
                    assert self.lower_row_invariant(row, col-1), "lower_row_invariant assertion for %d,%d failed!" % (row, col-1)
                else:
                    assert self.lower_row_invariant(row,0), "lower_row_invariant assertion for %d,%d failed!" % (row, 0)
                    print "\nCalling solve_col0_tile():"
                    move_string += self.solve_col0_tile(row)
                    assert self.lower_row_invariant(row-1,self.get_width()-1), "lower_row_invariant assertion for %d, %d failed!" % (row-1,self.get_width()-1)
        print "move_string:", move_string 
        print self.__str__()      

        print "\nPhase 2 ///////////////"
        # Second, solve rightmost j-2 cols of top two rows, 
        # right to left, bottom to top
        for col in range(self.get_width()-1, 1, -1):
            assert self.row1_invariant(col), "row1_invariant assertion for col %d failed!" % (col)
            print "\nCalling solve_row1_tile():"
            move_string += self.solve_row1_tile(col)
            print self.__str__()
            assert self.row0_invariant(col), "row0_invariant assertion for col %d failed!" % (col)
            print "\nCalling solve_row0_tile():"
            move_string += self.solve_row0_tile(col)
            print self.__str__()
        
        print "move_string:", move_string
        print self.__str__()

        print "\nPhase 3 //////////////"
        # Third and last, solve remaining 2x2 puzzle, 
        #i.e., top-left corner
        print "\nCalling solve_2x2():"
        move_string += self.solve_2x2()
        print self.__str__()

        # return string to solve puzzle
        print "\nFinal move string '%s'" % move_string
        print "\nFinal grid state:"
        print self.__str__()
        return move_string