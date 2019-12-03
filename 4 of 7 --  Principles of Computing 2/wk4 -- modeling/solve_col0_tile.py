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