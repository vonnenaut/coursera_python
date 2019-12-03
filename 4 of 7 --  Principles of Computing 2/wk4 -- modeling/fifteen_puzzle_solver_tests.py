import poc_simpletest
import fifteen_puzzle_solver_v1 as fpsolver

def print_grid(grid):
    for row in grid:
        print row
    print "\n"

def find_zero(grid):
    """
    finds location of zero tile in a grid
    returns a tuple
    """
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 0:
                return (row,col)

def run_suite():
    """
    Some informal testing code
    """    
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()
    test_number = 1
    index = 0


    # Run a series of tests on lower_row_invariant()
    print "\n------------------------------------------------------"
    print "Testing lower_row_invariant()\n"
    print "\n------------------------------------------------------"
    # test puzzle grids
    igrids = [[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]],
              [[4, 1, 8], [3, 0, 5], [6, 7, 2], [9, 10, 11]],
              [[4, 1, 2], [3, 0, 5], [6, 7, 8], [9, 10, 11]],
              [[4, 1, 2], [3, 0, 5], [6, 8, 10], [9, 7, 11]],
              [[11, 1, 2], [3, 4, 5], [6, 8, 10], [9, 7, 0]]]

    expected_outcomes = [True, 
                         False,
                         True,
                         False, 
                         True]

    for initial_grid in igrids:
        print "Test #%d:" % test_number
        print "Initial grid state:\n"
        game = fpsolver.Puzzle(len(initial_grid),len(initial_grid[0]),initial_grid)
        print_grid(initial_grid)
        suite.run_test(game.lower_row_invariant(find_zero(igrids[index])[0], find_zero(igrids[index])[1]), expected_outcomes[index], "Test #%d:" % test_number)
        print "\n------------------------------------------------------"
        test_number += 1
        index += 1


    # run a series of tests on solve_interior_tile()
    print "\n------------------------------------------------------"
    print "Testing solve_interior_tile()\n"
    print "\n------------------------------------------------------"
    # test puzzle grids
    igrids = [[[1, 3, 4], [2, 7, 5], [6, 8, 0], [9, 10, 11]],
              [[1, 3, 4], [2, 7, 5], [6, 0, 8], [9, 10, 11]],
              [[1, 3, 4], [2, 7, 5], [8, 6, 0], [9, 10, 11]],
              [[1, 3, 4], [2, 8, 5], [7, 6, 0], [9, 10, 11]],
              [[1, 3, 4], [2, 5, 11], [7, 6, 8], [9, 10, 0]],
              [[1, 3, 11], [2, 5, 4], [7, 6, 8], [9, 10, 0]],
              [[1, 3, 14], [2, 5, 4], [7, 6, 8], [9, 10, 11], [12, 13, 0]],
              [[1, 14, 3], [2, 5, 4], [7, 6, 8], [9, 10, 11], [12, 13, 0]],
              [[1, 5, 3], [2, 14, 4], [7, 6, 8], [9, 10, 11], [12, 13, 0]],
              [[8, 7, 6], [5, 4, 3], [2, 1, 0]],
              [[1, 3, 4], [2, 6, 5], [7, 8, 10], [9, 0, 11]],
              [[1, 3, 4], [2, 6, 10], [7, 8, 5], [9, 0, 11]],
              [[1, 3, 10], [2, 6, 4], [7, 8, 5], [9, 0, 11]]
            ]

    expected_outcomes = ["l", 
                         "uld",
                         "llurrdl",
                         "uldruld",
                         "uulddruld",
                         "uuulddrulddruld",
                         "uuuulddrulddrulddruld",
                         "uuuuldrulddrulddrulddruld",
                         "uuuldrulddrulddruld", 
                         "uulldrulddruldurrdl", 
                         "urullddruld", 
                         "uurullddrulddruld", 
                         "uuurdlludrulddrulddruld"]
    index = 0

    for initial_grid in igrids:
        print "Test #%d:" % test_number
        print "Initial grid state:\n"
        game = fpsolver.Puzzle(len(initial_grid),len(initial_grid[0]),initial_grid)
        print_grid(initial_grid)
        suite.run_test(game.solve_interior_tile(find_zero(igrids[index])[0], find_zero(igrids[index])[1]), expected_outcomes[index], "Test #%d:" % test_number)
        print "\n------------------------------------------------------"
        test_number += 1
        index += 1
    

    # run a series of tests on solve_col0_tile()
    print "\n------------------------------------------------------"
    print "Testing solve_col0_tile()\n"
    print "\n------------------------------------------------------"
    # test puzzle grids
    igrids = [[[2, 1, 5], [4, 6, 3], [0, 7, 8]],
              [[2, 1, 5], [4, 3, 6], [0, 7, 8]],
              [[2, 1, 3], [8, 4, 7], [6, 5, 9], [0, 10, 11]],
              [[7, 5, 1, 6], [2, 4, 3, 8], [0, 9, 10, 11], [12, 13, 14, 15]],
              [[11, 4, 3, 7, 12, 5], [2, 8, 1, 10, 9, 6], [0, 13, 14, 15, 16, 17]],
              [[8, 2, 10, 9, 1], [7, 6, 5, 4, 3], [0, 11, 12, 13, 14], [15, 16, 17, 18, 19]]
            ]

    expected_outcomes = ["urlruldrdlurdluurddlurr",
                         "urrulldruldrdlurdluurddlurr",
                         "urrulldruldrdlurdluurddlurr",
                         'urrrulldrulldruldrdlurdluurddlurrr',
                         'ururrrdlurdulldrulldrulldruldrdlurdluurddlurrrrr',
                         'urudruldrulldruldrdlurdluurddlurrrr'
                        ]
    index = 0

    for initial_grid in igrids:
        print "Test #%d:" % test_number
        print "Initial grid state:\n"
        game = fpsolver.Puzzle(len(initial_grid),len(initial_grid[0]),initial_grid)
        print_grid(initial_grid)
        suite.run_test(game.solve_col0_tile(find_zero(igrids[index])[0]), expected_outcomes[index], "Test #%d:" % test_number)
        print "\n------------------------------------------------------"
        test_number += 1
        index += 1


    # run a series of tests on row1_invariant()
    print "\n------------------------------------------------------"
    print "Testing row1_invariant()\n"
    print "\n------------------------------------------------------"
    print
    # test puzzle grids
    igrids = [[[2, 1, 5], [4, 3, 0], [6, 7, 8]],
              [[11, 1, 2, 3], [4, 5, 6, 7], [8, 9, 0, 10], [12, 13, 14, 15]],
              [[12, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 0, 14, 13]],
              [[12, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 0, 13, 14]],
              [[7, 1, 2, 3, 4], [5, 6, 0, 8, 9], [10, 11, 12, 13, 14]],
              [[4, 3, 2], [1, 0, 5], [6, 7, 8]]
             ]
    expected_outcomes = [True, False, False, False, True, True]
    index = 0

    for initial_grid in igrids:
        print "Test #%d:" % test_number
        print "Initial grid state:\n"
        game = fpsolver.Puzzle(len(initial_grid),len(initial_grid[0]),initial_grid)
        print_grid(initial_grid)
        suite.run_test(game.row1_invariant(find_zero(igrids[index])[1]), expected_outcomes[index], "Test #%d:" % test_number)
        print "\n------------------------------------------------------"
        test_number += 1
        index += 1    
    

    # run a series of tests on row0_invariant()
    print "\n------------------------------------------------------"
    print "Testing row0_invariant()\n"
    print "\n------------------------------------------------------"
    print
    # test puzzle grids
    igrids = [[[2, 1, 0], [3, 5, 4], [6, 7, 8]],
              [[2, 1, 0], [3, 4, 5], [6, 7, 8]],
              [[2, 1, 0, 3], [4, 5, 6, 7], [8, 9, 10, 11]],
              [[2, 1, 3, 0], [4, 5, 6, 7], [9, 8, 10, 11]],
              [[4, 2, 0, 3], [5, 1, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]],
              [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
             ]
    expected_outcomes = [False,  True, True, False, True, True]
    index = 0

    for initial_grid in igrids:
        print "Test #%d:" % test_number
        print "Initial grid state:\n"
        game = fpsolver.Puzzle(len(initial_grid),len(initial_grid[0]),initial_grid)
        print_grid(initial_grid)
        suite.run_test(game.row0_invariant(find_zero(igrids[index])[1]), expected_outcomes[index], "Test #%d:" % test_number)
        print "\n------------------------------------------------------"
        test_number += 1
        index += 1


    # run a series of tests on solve_row1_tile()
    print "\n------------------------------------------------------"
    print "Testing solve_row1_tile()\n"
    print "\n------------------------------------------------------"
    print
    # test puzzle grids
    igrids = [[[1, 2, 3, 7], [4, 5, 6, 0], [8, 9, 10, 11], [12, 13, 14, 15]],
              [[1, 6, 5, 4], [3, 7, 2, 0], [8, 9, 10, 11], [12, 13, 14, 15]],
              [[1, 5, 7, 4], [3, 6, 2, 0], [8, 9, 10, 11], [12, 13, 14, 15]],
              [[1, 7, 6, 4], [3, 5, 2, 0], [8, 9, 10, 11], [12, 13, 14, 15]],
              [[1, 6, 2, 4], [3, 5, 0, 7], [8, 9, 10, 11], [12, 13, 14, 15]],
             ]
    expected_outcomes = ["u",
                         "llurrdlur",
                         "uldruldur",
                         "ulldruldurrdlur",
                         "uldruldur",
                        ]
    index = 0

    for initial_grid in igrids:
        print "Test #%d:" % test_number
        print "Initial grid state:\n"
        game = fpsolver.Puzzle(len(initial_grid),len(initial_grid[0]),initial_grid)
        print_grid(initial_grid)
        suite.run_test(game.solve_row1_tile(find_zero(igrids[index])[1]), expected_outcomes[index], "Test #%d:" % test_number)
        print "\n------------------------------------------------------"
        test_number += 1
        index += 1


    # run a series of tests on solve_row0_tile()
    print "\n------------------------------------------------------"
    print "Testing solve_row0_tile()\n"
    print "\n------------------------------------------------------"
    print
    # test puzzle grids
    igrids = [[[4, 1, 0], [3, 2, 5]],
              [[3, 5, 4, 0], [2, 1, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
             ]
    expected_outcomes = ["lduldurdlurrdluldrruld",
                         "ldulduldrurdlurdlurrdluldrruld",
                        ]
    index = 0

    for initial_grid in igrids:
        print "Test #%d:" % test_number
        print "Initial grid state:\n"
        game = fpsolver.Puzzle(len(initial_grid),len(initial_grid[0]),initial_grid)
        print_grid(initial_grid)
        suite.run_test(game.solve_row0_tile(find_zero(igrids[index])[1]), expected_outcomes[index], "Test #%d:" % test_number)
        print "\n------------------------------------------------------"
        test_number += 1
        index += 1


    # run a series of tests on solve_puzzle()
    print "\n------------------------------------------------------"
    print "Testing solve_puzzle()\n"
    print "\n------------------------------------------------------"
    print
    # test puzzle grids
    igrids = [[[4, 2, 1], [3, 5, 0]],
              [[1, 2], [0, 4], [3, 5]],
              [[4, 1, 7], [2, 6, 5], [3, 0, 8]],
              [[8, 2, 11, 7], [6, 0, 4, 3], [9, 5, 1, 10]],
              [[4, 2, 10, 7, 9], [1, 0, 11, 8, 3], [17, 6, 18, 14, 12], [5, 19, 15, 16, 13]],
              [[1, 6, 5, 4], [3, 7, 2, 0], [8, 9, 10, 11], [12, 13, 14, 15]],
              [[16, 7, 13, 17, 5, 9], [3, 0, 14, 10, 12, 6], [4, 15, 2, 11, 8, 1]],
              
             ]

    expected_outcomes = ['lurlduldurdlurrdluldrruldulrdlurdlu',
                         'drlurlruldrdlurdluurddlurul',
                         'rluurdlludrulddruldurrulduldruldurdlurrdluldrruldulrdlu',
                         'drruuldrulddruldurullddruldlurudlurdlruldrdlurdluurddlurrruldllurrdlurdlurrdluldrruldulldruldurrdlurldlurdlurrdluldrruldul',
                         'ddrrrullldruldurrdlurrdllulldruldurrdllurlruldrdlurdluurddlurrrrllurrdlllurrdlurrlrulldrullddrulduurrlrdllurdlludrulddruldururrdlurdulldrulldruldrdlurdluurddlurrrrlurlduldruldurdlurrdluldrruldllurrdlurldlurdlurrdluldrruldlurldulrdlurdlu',
                         'dduldulduldurrruldulduldurrrllurrdlurldllurrdlurdlurrdluldrrulduldruldurldulrdlurdlu',
                         'drrrruulldrulddruldurrdluulllldrulddruldurrdlurrdlurrdluullldrulddruldurrdlurrdlllurrdluldururrrdlurdulldrulldrulldruldrdlurdluurddlurrrrrlllllurrdlurrdlurrdlurrdlurlduldurdlurrdluldrrulduldruldurldllurrdlurdlurrdluldrrulduldlurdlurrdluldrruldllurrdlurldlurdlurrdluldrruldulrdlurdlu'
                         
                         ]

    index = 0

    for initial_grid in igrids:
        print "Test #%d:" % test_number
        print "Initial grid state:\n"
        game = fpsolver.Puzzle(len(initial_grid),len(initial_grid[0]),initial_grid)
        print_grid(initial_grid)
        suite.run_test(game.solve_puzzle(), expected_outcomes[index], "Test #%d:" % test_number)
        print "\n------------------------------------------------------"
        test_number += 1
        index += 1

    suite.report_results()

run_suite()