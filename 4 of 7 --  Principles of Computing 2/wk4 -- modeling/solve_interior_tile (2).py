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
        # case 1: target tile is in same col as zero
        if ttile_col == zero_col:
            # ttile is above zero tile
            print "1a"
            temp_string += 'u' * (zero_row - ttile_row)
            # ttile is below zero tile
            print "1b"
            temp_string += 'd' * (zero_row - ttile_row)

        # case 2: target tile is in same row (to left or right of zero tile)
        elif ttile_row == zero_row:
            # ttile is to left of zero
            if ttile_col < zero_col:
                print "2a"
                temp_string += 'l' * (zero_col - ttile_col)
            # ttile is more than one
            elif ttile_col > zero_col+1:
                print "2b"
                temp_string += 'r' * (ttile_col - zero_col)
            # ttile row is above target_row
            elif ttile_col > zero_col and ttile_row == 0:
                if ttile_row < target_row:
                    temp_string += 'drul' + 'ddrul' * (target_row-ttile_row-1)
                
            # ttile is to right of zero and left of target
            # moves ttile right (going beneath)
                print "2b"
                temp_string += 'urdl' + ''
            # target row is not top row (move zero up and over)

        # ttile is to right of zero and target

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
        print "\nFinal grid state:"
        print clone.__str__()

        # update the puzzle and return the entire move string
        self.update_puzzle(move_string)
        return move_string