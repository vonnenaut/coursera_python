"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    result = []

    # populate result list with the same number of zeros as the length of the line parameter
    for index in range(len(line)):
        result.append(0)

    incr = 0

    # add non-zero line list parameter list elements to result list
    for index in range(len(line)):
        if line[index] != 0:
            result[incr] = line[index]
            incr += 1

    # create a copy of the result list to traverse so that result might be modified while traversing
    copy_of_list = result[:]

    # test for the same value in adjacent positions in the list and combine the found pairs, replacing the second value in each matching pair with a zero
    for index in range(1, len(copy_of_list)):
        if result[index] == result[index - 1]:
            result[index - 1] *= 2
            result[index] = 0

    # now that all pairs of like values have been combined, move everything of value to the left, grouping any zeros to the right
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

def merge_test_suite():
    """ Tests correct functionality of merge function """    
    line = [2, 0, 2, 4]
    print "\nTesting merge - Computed:", merge(line), "Expected:", [4, 4, 0, 0]
    
    line = [0, 0, 2, 2]
    print "\nTesting merge - Computed:", merge(line), "Expected:", [4, 0, 0, 0]
    
    line = [2, 2, 0, 0]
    print "\nTesting merge - Computed:", merge(line), "Expected:", [4, 0, 0, 0]
    
    line = [2, 2, 2, 2, 2]
    print "\nTesting merge - Computed:", merge(line), "Expected:", [4, 4, 2, 0, 0]
    
    line = [8, 16, 16, 8]
    print "\nTesting merge - Computed:", merge(line), "Expected:", [8, 32, 8, 0]
    
    line = [16, 16, 4, 2, 4, 4, 4]
    print "\nTesting merge - Computed:", merge(line), "Expected:", [32, 4, 2, 8, 4, 0, 0]
    
    line = [16, 0, 0, 0, 2, 0, 2]
    print "\nTesting merge - Computed:", merge(line), "Expected:", [16, 4, 0, 0, 0, 0, 0]

    line = [0, 64, 2, 64, 0, 2, 2]
    print "\nTesting merge - Computed:", merge(line), "Expected:", [64, 2, 64, 4, 0, 0, 0]



# merge_test_suite()
