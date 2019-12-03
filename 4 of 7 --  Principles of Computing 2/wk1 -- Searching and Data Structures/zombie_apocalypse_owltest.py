"""
Student portion of Zombie Apocalypse mini-project
"""

import poc_queue
# import random
import poc_grid
import poc_zombie_gui
# import poc_simpletest
import math

# global constants
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7



# Apocalypse class, a subclass of Grid
##
class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list=None,
                 zombie_list=None, human_list=None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)
        else:
            self._human_list = []

    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self._zombie_list = []
        self._human_list = []

        poc_grid.Grid.clear(self)

    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        if self.is_empty(row, col):
            self._zombie_list.append((row, col))

    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)

    def zombies(self):
        """
        Generator that yields zombies in the order they were
        added.
        """
        # zombie_copies = self._zombie_list[:]

        # for zombie in self._zombie_list:
        #     yield zombie
        # alternate syntax
        return (zombie for zombie in self._zombie_list)

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        if self.is_empty(row, col):
            self._human_list.append((row, col))

    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)

    def humans(self):
        """
        Generator that yields humans in the order they were added.
        """
        return (human for human in self._human_list)

    def _manhattan_distance(self, row0, col0, row1, col1):
        """ 
        Computes Manhattan distance between two cells.

        Returns an int.
        """
        return abs(row0 - row1) + abs(col0 - col1)

    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        visited = poc_grid.Grid(self.get_grid_height(), self.get_grid_width())
        distance_field = [[self.get_grid_width() * self.get_grid_height() for dummy_col in range(
            self.get_grid_width())] for dummy_row in range(self.get_grid_height())]
        
        boundary = poc_queue.Queue()
        entity_list = []

        if entity_type == ZOMBIE:
            for zombie in self.zombies():
                boundary.enqueue(zombie)
                entity_list.append(zombie)
        elif entity_type == HUMAN:
            for human in self.humans():
                boundary.enqueue(human)
                entity_list.append(human)
        else:
            print "Invaid entity type in compute_distance_field()!"
            return

        for entity in boundary.__iter__():
            visited.set_full(entity[0],entity[1])
            distance_field[entity[0]][entity[1]] = 0
            
        current_cell = None

        while boundary.__len__() > 0:
            current_cell = boundary.dequeue()

            if entity_type == "ZOMBIE":
                neighbors = self.eight_neighbors(current_cell[0], current_cell[1])
            else:
                neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            
            for neighbor_cell in neighbors:
                if visited.is_empty(neighbor_cell[0],neighbor_cell[1]) and self.is_empty(neighbor_cell[0],neighbor_cell[1]):
                    visited.set_full(neighbor_cell[0],neighbor_cell[1])
                    if neighbor_cell == (14,14):    # These
                        print current_cell          # lines
                        return distance_field       # added
                    boundary.enqueue(neighbor_cell)
                    distance = min([self._manhattan_distance(entity[0],entity[1],current_cell[0],current_cell[1]) for entity in entity_list])
                    distance_field[neighbor_cell[0]][neighbor_cell[1]] = distance + 1

        return distance_field

    def print_field(self, field):
        """
        Prints distance field in grid format 
        """
        for row in field:
            print row
        print "\n"

    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for human in self.humans():
            print "human:", human
            best_value = zombie_distance_field[int(human[0])][int(human[1])]
            best_location = human

            for neighbor in self.eight_neighbors(human[0], human[1]):
                if zombie_distance_field[neighbor[0]][neighbor[1]] > best_value and self.is_empty(neighbor[0],neighbor[1]):
                    best_location = (neighbor[0], neighbor[1])

            self._human_list[self._human_list.index(human)] = best_location


    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for zombie in self.zombies():
            print "zombie:", zombie
            best_value = human_distance_field[int(zombie[0])][int(zombie[1])]
            best_location = zombie

            for neighbor in self.four_neighbors(zombie[0], zombie[1]):
                if human_distance_field[neighbor[0]][neighbor[1]] < best_value and self.is_empty(neighbor[0],neighbor[1]):
                    best_location = (neighbor[0], neighbor[1])
            
            print "best_location:", best_location
            self._zombie_list[self._zombie_list.index(zombie)] = best_location
        
# Start up gui for simulation - You will need to write some code above
# before this will work without errors

# poc_zombie_gui.run_gui(Apocalypse(10, 8))


# def run_suite():
#     """
#     Some informal testing code
#     """
#     # create a TestSuite object
#     suite = poc_simpletest.TestSuite()

#     # Owltest Troubleshooting
#     # 1.
#     # [-15.0 pts] For 
#     # obj = Apocalypse(3, 3, [], [(2, 2)], [(1, 1)])
#     # dist = [[4, 3, 2], [3, 2, 1], [2, 1, 0]]
#     # obj.move_humans(dist)
#     # for human in obj.humans():
#     #     print human
#     # suite.run_test(obj.move_humans(dist), [(0, 0)], "Test #1:")

#     # 2.
#     # [-15.0 pts] For
#     # obj = Apocalypse(3, 3, [], [(1, 1)], [(1, 1)])
#     # dist = [[2, 1, 2], [1, 0, 1], [2, 1, 2]]
#     # print "zombies:"
#     # for zombie in obj.zombies():
#     #     print zombie
#     # obj.move_zombies(dist)
#     # print "zombies:"
#     # for zombie in obj.zombies():
#     #     print zombie
#     # suite.run_test(obj.zombies(), [(1, 1)], "Test #2:")
#     # # but received [(1, 2)]

#     # [-7.5 pts] For 
#     obj = Apocalypse(20, 30, [(4, 15), (5, 15), (6, 15), (7, 15), (8, 15), (9, 15), (10, 15), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (15, 14), (15, 13), (15, 12), (15, 11), (15, 10)], [], [(18, 14), (18, 20), (14, 24), (7, 24), (2, 22)])
#     output = obj.compute_distance_field(HUMAN)
#     print "Expected:"
#     print "[24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 3, 4, 5, 6, 7, 8, 9]"
#     print "[23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 7, 8]"
#     print "[22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8  7, 6, 5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 6, 7]"
#     print "[23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 7, 8]"
#     print "[24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11  10, 600, 8, 7, 6, 5, 4, 3, 2, 3, 3, 4, 5, 6, 7, 8]"
#     print "[25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 600, 9, 8, 7, 6, 5, 4, 3, 3, 2, 3, 4, 5, 6, 7]"
#     print "[26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 600, 9, 8, 7, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6]"
#     print "[25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 17, 16, 15, 14, 13, 600, 8, 7, 6, 5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5]"
#     print "[ 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 16, 17, 16, 15, 14, 600, 9, 8, 7, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6,"
#     print "[ 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 15, 16, 17, 16, 15, 600,10, 9, 8, 7, 6, 5, 4, 3, 2, 3, 4, 5, 6, 7,"
#     print "[ 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 14, 15, 16, 17, 16, 600,10,10, 9, 8, 7, 6, 5, 4, 3, 4, 5, 6, 7, 8,"
#     print "[ 21, 20, 19, 18, 17, 16,  15, 14, 13, 12, 13, 14, 15, 16, 17, 600, 9,10, 9, 8, 7, 6, 5, 4, 3, 4, 5, 6, 7, 8,"
#     print "[ 20, 19, 18, 17, 16, 15,  14, 13, 12, 11, 12, 13, 14, 15, 16, 600, 8, 9, 8, 7, 6, 5, 4, 3, 2, 3, 4, 5, 6, 7,"
#     print "[ 19, 18, 17, 16, 15, 14,  13, 12, 11, 10, 11, 12, 13, 14, 15, 600, 7, 8, 7, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6,"
#     print "[ 18, 17, 16, 15, 14, 13,  12, 11, 10, 9, 10, 11, 12, 13, 14, 600, 6, 7, 6, 5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5,"
#     print "[ 17, 16, 15, 14, 13, 12,  11, 10,  9, 8, 600,600,600,600,600, 600, 5, 6, 5, 4, 3, 4, 3, 2, 1, 2, 3, 4, 5, 6,"
#     print "[ 16, 15, 14, 13, 12, 11, 10,  9,  8,  7, 6, 5, 4, 3, 2, 3, 4, 5, 4, 3, 2, 3, 4, 3, 2, 3, 4, 5, 6, 7,"
#     print "[ 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8,"
#     print "[ 14, 13, 12, 11, 10, 9  8, 7, 6, 5, 4, 3, 2, 1, 0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,"
#     print  "[15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"

#     print "\nActual:"
#     for row in output:
#         print row

# run_suite()

# Test
obj = Apocalypse(20, 30, [(4, 15), (5, 15), (6, 15), (7, 15), (8, 15), (9, 15), (10, 15), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (15, 14), (15, 13), (15, 12), (15, 11), (15, 10)], [], [(18, 14), (18, 20), (14, 24), (7, 24), (2, 22)])
df = obj.compute_distance_field(HUMAN)
for row in df:
    for elem in row:
        print "%3d"% elem,
    print