"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    result = []

    for index in range(len(line)):
        result.append(0)

    increment = 0

    for index in range(len(line)):
        if line[index] != 0:
            result[increment] = line[index]
            increment += 1
    # print "Result1: ",result

    copy_of_list = result[:]

    for index in range(len(copy_of_list) - 2):
        if copy_of_list[index] == copy_of_list[index + 1]:
            result[index] *= 2
            result[index + 1] = 0
            # print "Result2: ", result
        if copy_of_list[index + 2] != 0:
        	result[index + 1] = result[index + 2]
        	result[index + 2] = 0
        	# print "Result3: ", result
        else:
      		result[index + 1] = 0 
            # print "Result4: ",result
    return result

# Test
# results should be:
# R1:  [4, 4, 0, 0]
# R2:  [4, 0, 0, 0]
# R3:  [4, 0, 0, 0]
# R4:  [4, 4, 2, 0, 0]
# R5:  [8, 32, 8, 0]

# line = [2, 0, 2, 2]
# print "\nR1: ",merge(line)

# line = [0, 0, 2, 2]
# print "\nR2: ",merge(line)

# line = [2, 2, 0, 0]
# print "\nR3: ",merge(line)

# line = [2, 2, 2, 2, 2]
# print "\nR4: ",merge(line)

# line = [8, 16, 16, 8]
# print "\nR5: ",merge(line)


