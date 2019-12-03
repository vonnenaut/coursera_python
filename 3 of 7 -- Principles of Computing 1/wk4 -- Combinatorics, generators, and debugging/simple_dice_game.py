""" Analyzing a Simple Dice Game 
"""
def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length
    """
    ans = set([()])
    for dummy_idx in range(length):
        temp = set()
        for seq in ans:
            for item in outcomes:
                new_seq = list(seq)
                new_seq.append(item)
                temp.add(tuple(new_seq))
        ans = temp
    return ans


def max_repeats(outcomes, seq):
    """ 
    Takes a sequence and computes the maximum number of times that any individual item occurs in the sequence.

    Returns a list whose index represents the value of the die number and whose value represents the number of times that die number was rolled.
    """
    max_times = [seq.count(value) for value in outcomes if value > 0]
    # print "max_times:", max_times
    # print "max value:", max_times.index(max(max_times)) + 1
    return max_times


def compute_expected_value(outcomes):
    """ 
    Computes expected value excluding initial $10 paid.
    Should lie in the range of $9 - 11.

    No double or triples:  $0
    Doubles:  $10 (break even)
    Triples:  $200
    probability of any one roll:  1/216
    """
    all_seq = gen_all_sequences(outcomes, 3)
    triples = 0
    doubles = 0
    exp_value = 0.0

    for rolls in all_seq:
    	if 3 in max_repeats(outcomes, rolls):
    		triples += 1
    	elif 2 in max_repeats(outcomes, rolls):
    		doubles += 1
    for value in range(1,7):
    	exp_value += value*90/float(216)
    for value in range(1,7):
    	exp_value += value*6/float(216)
   
    # print "triples:", triples
    # print "doubles:", doubles
    # print "expected value:"
    return exp_value



def run_test():
	""" 
	Testing code.  Note that the initial cost of playing the game has been subtracted.
	"""
	outcomes = set([1, 2, 3, 4, 5, 6])
    print "All possible sequences of three dice are"
    print gen_all_sequences(outcomes, 3)
    print
    print "Test for max repeats"
    print "Max repeat for (3, 1, 2) is", max_repeats(outcomes, (3, 1, 2))
    print "Max repeat for (3, 3, 2) is", max_repeats(outcomes, (3, 3, 2))
    print "Max repeat for (3, 3, 3) is", max_repeats(outcomes, (3, 3, 3))
    print
    print "Ignoring the initial $10, the expected value was $", compute_expected_value(outcomes)
    
run_test()