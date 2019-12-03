# wk 1 quiz, 39

def appendsums(lst): 
    """ 
    Repeatedly append the sum of the current last three elements 
    of lst to lst. 
    """
    for iter in range(25):
    	lst.append(lst[-1] + lst[-2] + lst[-3])
    return lst

# Question
sum_three = [0, 1, 2]
appendsums(sum_three)
print sum_three[10]
print "sum_three[20]: ", sum_three[20]