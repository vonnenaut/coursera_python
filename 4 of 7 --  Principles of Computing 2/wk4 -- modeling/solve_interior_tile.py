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