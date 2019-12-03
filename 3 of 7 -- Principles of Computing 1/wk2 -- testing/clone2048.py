"""
Coursera Principles of Computing 1
Clone of 2048 game.
Daniel Ashcom
03/22/17
"""

import random
# import poc_simpletest
# import poc_2048_gui

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    result = []

    # populate result list with same number of zeros as the length of the line
    # parameter
    for index in range(len(line)):
        result.append(0)

    incr = 0

    # add non-zero line list parameter list elements to result list
    for index in range(len(line)):
        if line[index] != 0:
            result[incr] = line[index]
            incr += 1

    # create a copy of the result list to traverse so that result might be
    # modified while traversing
    copy_of_list = result[:]

    # test for the same value in adjacent positions in the list and combine
    # the found pairs, replacing the second value in each matching pair with a
    # zero
    for index in range(1, len(copy_of_list)):
        if result[index] == result[index - 1]:
            result[index - 1] *= 2
            result[index] = 0

    # now that all pairs of like values have been combined, move everything of
    # value to the left, grouping any zeros to the right
    copy_of_list = result[:]
    result = []

    for index in range(len(copy_of_list)):
        result.append(0)

    incr = 0

    for index in range(len(copy_of_list)):
        if copy_of_list[index] != 0:
            result[incr] = copy_of_list[index]
            incr += 1

    return result


class TwentyFortyEight:
    """
    main class which runs game logic
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height     # number of rows
        self._grid_width = grid_width       # number of columns
        self._rand_num_range = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
        self._tiles = []      # stores the values in each cell of the grid
        self._initial_indices = {}
        self._offsets = OFFSETS
        # tracks whether list has changed in order to spawn a new tile
        self._list_changed = False
        self._game_lost = False
        self.create_initial_indices()
        self.reset()        

    def create_initial_indices(self):
        """ dynamically creates set of initial indices for use in traversing grid """
      
        # temporarily holds values for each direction's initial indices (a list
        # of tuples) to be added to a dictionary with direction numbers as keys
        # (1, 2, 3, 4)
        temp_list = []
        directions = [UP, DOWN, LEFT, RIGHT]
        width = self.get_grid_width()
        height = self.get_grid_height()

        option_num_steps = {UP: width,
                            DOWN: width,
                            LEFT: height,
                            RIGHT: height}

        option_starting_index = {UP: [0, 0],
                                 DOWN: [height-1, 0],
                                 LEFT: [0, 0],
                                 RIGHT: [0, width-1]}

        option_offset = {UP: LEFT,
                         DOWN: LEFT,
                         LEFT: UP,
                         RIGHT: UP}

        # create initial indices for all four directions of play
        for direction in directions:
            for num_steps in range(option_num_steps[direction]):
                row = option_starting_index[direction][0] + num_steps * \
                    self.get_offset(option_offset[direction])[0]
                col = option_starting_index[direction][1] + num_steps * \
                    self.get_offset(option_offset[direction])[1]
                temp_list.append(tuple([row, col]))

            # print direction, temp_list
            self._initial_indices[direction] = temp_list
            temp_list = []

    def reset(self):
        """
        Reset the game so the grid is empty except for two initial tiles. """
        self._tiles = [[0 for dummy_col in range(
            self.get_grid_width())] for dummy_row in range(self.get_grid_height())]

        for dummy_var in range(2):  # add two initial tiles to the empty grid
            self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        string = ""

        for row in range(len(self._tiles)):
            string += str(self._tiles[row]) + '\n'

        return string

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._grid_width

    def get_rand_value(self):
        """ return a random value with 90% chance of it being 2 and 10% chance of it being 4 """
        return self._rand_num_range[random.randrange(0, 10)]

    def get_offset(self, direction):
        """ returns the offset (tuple) for a given direction """
        return self._offsets[direction]

    def get_tiles_indices(self, direction):
        """ returns the initial indices (a list of tuples) for a given direction """
        return self._initial_indices[direction]

    def traverse_grid(self, start_cell, direction, num_steps):
        """ helper method for move, allowing traversal of a row or column.
            This method returns the values of that row or column. """
        _values_list = []

        for step in range(num_steps):
            row = start_cell[0] + step * direction[0]
            col = start_cell[1] + step * direction[1]
            # print "row, col: (line 202)", row, col
            _values_list.append(self.get_tile(row, col))

        return _values_list

    def set_grid(self, start_cell, direction, num_steps, value_list):
        """ helper method for move, allowing traversal of a row or column.
            This method sets the values of that row or column. """
        index = 0

        for step in range(num_steps):
            row = start_cell[0] + step * direction[0]
            col = start_cell[1] + step * direction[1]
            # print "row, col: (line 217)"
            old_value = self.get_tile(row, col)
            new_value = self.set_tile(row, col, value_list[index])
            index += 1

            if old_value != new_value:
                self._list_changed = True

    def count_empty_tiles(self):
        """ returns the number of remaining empty cells to check whether game is lost """
        count = 0

        for tile in self.get_tiles_indices(UP):
            num_zeros = self.traverse_grid(
                tile, self.get_offset(UP), self.get_grid_height()).count(0)
            count += num_zeros
        return count

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles have moved.
        """
        # 1. iterate over starting cell indices, calling traverse_grid on each index to process that row/col, returning a list of values for that row/col
        # 2. pass the row/col list to merge to process it
        # 3. iterate over the row/col again to store merged tile values list
        # back into the grid and check if anything has changed, adding a new
        # tile if so.
        temp_list = []

        if direction in [1, 2]:
            num_steps = self.get_grid_height()
        else:
            num_steps = self.get_grid_width()

        if self.count_empty_tiles() > 0:
            # 1
            for tile in self.get_tiles_indices(direction):
                # 2
                temp_list = merge(self.traverse_grid(
                    tile, self.get_offset(direction), num_steps))
                # 3
                self.set_grid(tile, self.get_offset(
                    direction), num_steps, temp_list)

            # if anything has moved on the grid, spawn a new tile randomly
            if self._list_changed is True and self._game_lost is False:
                self.new_tile()
                self._list_changed = False
        else:
            _game_lost = True

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.  This method calls itself recursively until it randomly gets a blank tile to populate with a value.
        """
        row = random.randrange(self.get_grid_height())
        col = random.randrange(self.get_grid_width())
        # set tile's value equal to a value randomly selected from a list which
        # ensures probabilities mentioned above.
        value = self.get_rand_value()

        if self.get_tile(row, col) == 0:
            self.set_tile(row, col, value)
            return True
        else:
            self.new_tile()

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._tiles[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._tiles[row][col]


# class run_test_suite():
#     """ Testing suite for TwentyFortyEight class """

#     def __init__(self):
#         # create a TestSuite object
#         self.suite = poc_simpletest.TestSuite()
#         # create a TwentyFortyEight object
#         self.game = TwentyFortyEight(4, 4)

#     def print_grid(self):
#         """ prints the game board for testing porpoises """
#         for row in range(len(self.game._tiles)):
#             print self.game._tiles[row]
#         print "\n"

#     def run_tests(self):
        # Test get_grid_height
        # self.suite.run_test(self.game.get_grid_height(), GRID_HEIGHT, "Test #1:")
        # # Test get_grid_width
        # self.suite.run_test(self.game.get_grid_width(), 5, "Test #2:")
        # # # Test set_tile
        # self.suite.run_test(self.game.set_tile(0, 0, 64), None, "Test #3:")
        # self.suite.run_test(self.game.set_tile(2, 3, 256), None, "Test #4")
        # # # Test get_tile
        # self.suite.run_test(self.game.get_tile(0, 0), 64, "Test #5:")
        # # Test new_tile
        # self.suite.run_test(self.game.new_tile(), True, "Test #6:")
        # # Test traverse_grid
        # self.print_grid()
        # self.suite.run_test(self.game.traverse_grid((0, 0), (0, 1),
        # GRID_WIDTH), self.game._tiles[0], "Test #7:")

        # # reset board
        # self.game.reset()
        # self.print_grid()

        # # Test merge
        # line = [2, 0, 2, 4]
        # self.suite.run_test(merge(line), [4, 4, 0, 0], "Test #8:")

        # line = [0, 0, 2, 2]
        # self.suite.run_test(merge(line), [4, 0, 0, 0], "Test #9:")

        # line = [2, 2, 0, 0]
        # self.suite.run_test(merge(line), [4, 0, 0, 0], "Test #10:")

        # line = [2, 2, 2, 2, 2]
        # self.suite.run_test(merge(line), [4, 4, 2, 0, 0], "Test #11:")

        # line = [8, 16, 16, 8]
        # self.suite.run_test(merge(line), [8, 32, 8, 0], "Test #12:")

        # line = [16, 16, 4, 2, 4, 4, 4]
        # self.suite.run_test(merge(line), [32, 4, 2, 8, 4, 0, 0], "Test #13:")

        # line = [16, 0, 0, 0, 2, 0, 2]
        # self.suite.run_test(merge(line), [16, 4, 0, 0, 0, 0, 0], "Test #14:")

        # line = [0, 64, 2, 64, 0, 2, 2]
        # self.suite.run_test(merge(line), [64, 2, 64, 4, 0, 0, 0], "Test
        # #15:")

        # # Test move
        # print "Test #16 before:"
        # self.print_grid()
        # self.suite.run_test(self.game.move(UP), None, "Test #16:")
        # print "Test #16 after:"
        # self.print_grid()

        # # Test __str__
        # self.suite.run_test(self.game.__str__(), self.game, "Test #17:")

        # # print a report of final test results
        # print "\n"
        # self.suite.report_results()




## OwlTests:
# option_starting_index = {UP: [0, 0],
#                          DOWN: [((self.get_grid_height()) - 1), 0],
#                          LEFT: [0, 0],
#                          RIGHT: [0, ((self.get_grid_height()) - 1)]}


# OwlTest #1 
# requires self.get_grid_height() - 1 for DOWN and RIGHT to pass
# obj = TwentyFortyEight(4, 4)
# # # Test __str__
# # # print obj
# # # Test get_tiles_indices
# print obj.get_tiles_indices(RIGHT)

# obj.set_tile(0, 0, 2)
# obj.set_tile(0, 1, 0)
# obj.set_tile(0, 2, 0)
# obj.set_tile(0, 3, 0)
# obj.set_tile(1, 0, 0)
# obj.set_tile(1, 1, 2)
# obj.set_tile(1, 2, 0)
# obj.set_tile(1, 3, 0)
# obj.set_tile(2, 0, 0)
# obj.set_tile(2, 1, 0)
# obj.set_tile(2, 2, 2)
# obj.set_tile(2, 3, 0)
# obj.set_tile(3, 0, 0)
# obj.set_tile(3, 1, 0)
# obj.set_tile(3, 2, 0)
# obj.set_tile(3, 3, 2)

#OwlTest #2
# requires self.get_grid_height() for DOWN and RIGHT to pass
# obj = TwentyFortyEight(5, 6)
# obj.set_tile(0, 0, 0)
# obj.set_tile(0, 1, 2)
# obj.set_tile(0, 2, 4)
# obj.set_tile(0, 3, 8)
# obj.set_tile(0, 4, 8)
# obj.set_tile(0, 5, 32)
# obj.set_tile(1, 0, 16)
# obj.set_tile(1, 1, 2)
# obj.set_tile(1, 2, 4)
# obj.set_tile(1, 3, 16)
# obj.set_tile(1, 4, 64)
# obj.set_tile(1, 5, 32)
# obj.set_tile(2, 0, 0)
# obj.set_tile(2, 1, 2)
# obj.set_tile(2, 2, 4)
# obj.set_tile(2, 3, 8)
# obj.set_tile(2, 4, 0)
# obj.set_tile(2, 5, 32)
# obj.set_tile(3, 0, 16)
# obj.set_tile(3, 1, 16)
# obj.set_tile(3, 2, 16)
# obj.set_tile(3, 3, 16)
# obj.set_tile(3, 4, 16)
# obj.set_tile(3, 5, 16)
# obj.set_tile(4, 0, 16)
# obj.set_tile(4, 1, 8)
# obj.set_tile(4, 2, 4)
# obj.set_tile(4, 3, 4)
# obj.set_tile(4, 4, 16)
# obj.set_tile(4, 5, 2)


#OwlTest #3
obj = TwentyFortyEight(4, 4)
obj.set_tile(0, 0, 2)
obj.set_tile(0, 1, 4)
obj.set_tile(0, 2, 8)
obj.set_tile(0, 3, 16)
obj.set_tile(1, 0, 16)
obj.set_tile(1, 1, 8)
obj.set_tile(1, 2, 4)
obj.set_tile(1, 3, 2)
obj.set_tile(2, 0, 0)
obj.set_tile(2, 1, 0)
obj.set_tile(2, 2, 8)
obj.set_tile(2, 3, 16)
obj.set_tile(3, 0, 0)
obj.set_tile(3, 1, 0)
obj.set_tile(3, 2, 4)
obj.set_tile(3, 3, 2)


print "Before move call:"
for row in range(len(obj._tiles)):
    print obj._tiles[row]
print "\n"

obj.move(UP)

# print "Expected:"
# print "[[0, 0, 2, 4, 16, 32]\n[16, 2, 4, 16, 64, 32]\n [0, 0, 2, 4, 8, 32]\n[0, 0, 0, 32, 32, 32]\n[0, 16, 8, 8, 16, 2]] with 1 additional tile"

print "After:"
for row in range(len(obj._tiles)):
    print obj._tiles[row]
print "\n"


# Start test suite  --  simply comment these two lines out to disable testing
# test = run_test_suite()
# test.run_tests()

# game = TwentyFortyEight(4, 3)


# Start GUI
# poc_2048_gui.run_gui(TwentyFortyEight(GRID_HEIGHT, GRID_WIDTH))
