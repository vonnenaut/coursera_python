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

    incr = 0

    for index in range(len(line)):
        if line[index] != 0:
            result[incr] = line[index]
            incr += 1

    copy_of_list = result[:]

    for index in range(1,len(copy_of_list)):
    	if result[index] == result[index - 1]:
    		result[index - 1] *= 2
    		result[index] = 0

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


# Test
# results should be:
# R1:  [4, 4, 0, 0]
# R2:  [4, 0, 0, 0]
# R3:  [4, 0, 0, 0]
# R4:  [4, 4, 2, 0, 0]
# R5:  [8, 32, 8, 0]

# line = [2, 0, 2, 4]
# print "\nR1: ",merge(line)
# 
# line = [0, 0, 2, 2]
# print "\nR2: ",merge(line)
# 
# line = [2, 2, 0, 0]
# print "\nR3: ",merge(line)
# 
# line = [2, 2, 2, 2, 2]
# print "\nR4: ",merge(line)
# 
# line = [8, 16, 16, 8]
# print "\nR5: ",merge(line)


