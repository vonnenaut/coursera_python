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
            print "case 1"
            return ''

        # recursive case
        # move zero tile from (0,j) to (1,j-1)
        elif zero_row != 1 or zero_col != (target_col-2) or ttile_row != 1 or ttile_col != (target_col-1):
            if zero_row == 0 and zero_col == target_col:
                print "case 2a"
                temp_string += 'ld'
            # move ttile to (1,j-1) and zero to (1,j-2)
            elif ttile_col == zero_col:
                print "case 2b"
                temp_string += 'uld'
            # elif ttile_col < zero_col:
            elif ttile_col < zero_col and zero_row == 1:
                print "case 2c"
                temp_string += 'u' + 'l' * (zero_col - ttile_col)
            elif zero_row == 0 and zero_col == (ttile_col-1) and ttile_row == 0:
                print "case 2d"
                temp_string += 'dr'
            elif ttile_col == target_col-2 and ttile_row == 1 and zero_col == ttile_col-1 and zero_row == 1:
                temp_string += 'urrdl'
            print "temp_string", temp_string
        # once zero and ttile are in place, move ttile to final location
        else:
            print "case 3"
            temp_string += 'urdlurrdluldrruld'
            
        # recursive call
        move_string += temp_string 
        clone.update_puzzle(move_string)
        clone.get_zero_pos()
        print "\nRecursive call //////////"
        move_string += clone.solve_row0_tile(target_col)
        self.update_puzzle(move_string)
        print "final grid state:"
        print self.__str__()
        return move_string