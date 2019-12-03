"""
Student portion of Zombie Apocalypse mini-project
"""

import poc_queue
import random
import poc_grid
import poc_zombie_gui
import poc_simpletest
import math

# global constants
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


"""
Apocalypse class, a subclass of Grid
"""


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
        zombie_copies = self._zombie_list[:]

        for zombie in self._zombie_list:
            yield zombie
        # alternate syntax
        # return (zombie for zombie in self._zombie_list)

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
        human_copies = self._human_list[:]

        for human in human_copies:
            yield human
        # alternate syntax
        # return (human for human in self._human_list)

    def manhattan_distance(self, row0, col0, row1, col1):
        """ 
        Computes Manhattan distance between two cells.

        Returns an int.
        """
        return abs(row0 - row1) + abs(col0 - col1)

    def create_distance_field(self, entity_list):
        """
        Creates manhattan distance field which contains minimum distance to each entity in entity_list.
        Each entity is represented as a grid position (row, col)
        """
        distance_field = [[self.get_grid_width() * self.get_grid_height() for dummy_col in range(
            self.get_grid_width())] for dummy_row in range(self.get_grid_height())]
        
        for row in range(self.get_grid_height()):
            for col in range(self.get_grid_width()):
                distance = min([self.manhattan_distance(entity[0], entity[1], row, col) for entity in entity_list])
                distance_field[row][col] = distance_field
        return distance_field

    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        visited = poc_grid.Grid(self.get_grid_height(), self.get_grid_width())
        distance_field = [[self.get_grid_width() * self.get_grid_height() for dummy_col in range(
            self.get_grid_width())] for dummy_row in range(self.get_grid_height())]

        # Create a queue, boundary, that is a *copy* of either the zombie list or the human list. For cells in the queue, initialize visited to be FULL and distance_field to be zero. We recommend that you use our Queue class.
        boundary = poc_queue.Queue()

        if entity_type == ZOMBIE:
            for zombie in self.zombies():
                boundary.enqueue(zombie)
        elif entity_type == HUMAN:
            for human in self.humans():
                boundary.enqueue(human)
        else:
            print "Invaid entity type in compute_distance_field()!"
            return

        for entity in boundary.__iter__():
            visited.set_full(entity[0],entity[1])
            distance_field[entity[0]][entity[1]] = 0
            
        current_cell = None

        while boundary.__len__() > 0:
            print "--------------------------"
            # print "boundary queue:", boundary

            current_cell = boundary.dequeue()

            print "current_cell:", current_cell
            print "boundary queue:", boundary

            if entity_type == "ZOMBIE":
                neighbors = self.eight_neighbors(current_cell[0], current_cell[1])
            else:
                neighbors = self.four_neighbors(current_cell[0], current_cell[1])

            print "\nneighbors of ", current_cell, ":"
            print neighbors

            for neighbor_cell in neighbors:
                print "neighbor_cell:", neighbor_cell
                if visited.is_empty(neighbor_cell[0],neighbor_cell[1]) and self.is_empty(neighbor_cell[0],neighbor_cell[1]):
                    visited.set_full(neighbor_cell[0],neighbor_cell[1])
                    boundary.enqueue(neighbor_cell)
                    distance_field[neighbor_cell[0]][neighbor_cell[1]] = self.manhattan_distance(neighbor_cell[0],current_cell[0], neighbor_cell[1], current_cell[1])
                    # distance_field = self.create_distance_field([neighbor_cell, current_cell])
                    print "distance_field[neighbor_cell[0]][neighbor_cell[1]]:", distance_field[neighbor_cell[0]][neighbor_cell[1]]

                    print "\nvisited:\n", visited
                    print "distance_field:"
                    self.print_field(distance_field)

        print "\nvisited:\n", visited
        print "\ndistance_field:\n"
        self.print_field(distance_field) 

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
        pseudocode:
        for each human:
            for each neighbor:
                set the highest value as the move target (furthest from a zombie)
            move the human to the furthest distance from a zombie
        """
        best_location = 0

        for human in self.humans():
            for neighbor in self.eight_neighbors(human[0], human[1]):
                if zombie_distance_field[neighbor[0]][neighbor[1]] > best_location and self.is_empty(neighbor[0],neighbor[1]):
                    best_location = (neighbor[0], neighbor[1])
            # move human to neighboring location furthest from any zombies
            self._human_list[self._human_list.index(human)] = best_location


    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        best_location = self.get_grid_height()*self.get_grid_width()

        for zombie in self.zombies():
            for neighbor in self.four_neighbors(zombie[0], zombie[1]):
                if human_distance_field[neighbor[0]][neighbor[1]] < best_location and self.is_empty(neighbor[0],neighbor[1]):
                    best_location = (neighbor[0], neighbor[1])
            # move human to neighboring location furthest from any zombies
            self._zombie_list[self._zombie_list.index(zombie)] = best_location
        

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

# poc_zombie_gui.run_gui(Apocalypse(10, 8))


"""
Testing Apparatus for Zombie Apocalypse mini-project
"""
# import poc_simpletest
# import zombie_apocalypse


def run_suite(format_function):
    """
    Some informal testing code
    """
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()
    # create an instance of the Apocalypse class
    # obstacle_list = []
    obstacle_list = [(2,0), (2,2)]
    # zombie_list = []
    zombie_list = [(0,0),(0,2)]
    # human_list = []
    human_list = [(3,0), (3,2)]
    # apoc = Apocalypse(5, 3)
    apoc = Apocalypse(5, 3, obstacle_list, zombie_list, human_list)

    def test_manhattan_distance():
        print "\nTesting manhattan_distance:"
        current_cell = (1,0)
        neighbors = [(1,1)]
        for neighbor_cell in neighbors:
            print neighbor_cell, ":", apoc.manhattan_distance(neighbor_cell, current_cell)

    def test_compute_dist_field():
        print "ZOMBIE distance_field:"
        apoc.compute_distance_field(ZOMBIE)
        # print "HUMAN distance_field:"
        # apoc.compute_distance_field(HUMAN)
    
    if format_function == "all":        
        test_manhattan_distance()
        test_compute_dist_field()        
    elif format_function == "manhattan_distance":
        test_manhattan_distance()
    elif format_function == "compute_distance_field":
        test_compute_dist_field()
    

    suite.report_results()

run_suite("compute_distance_field")
# run_suite("manhattan_distance")


