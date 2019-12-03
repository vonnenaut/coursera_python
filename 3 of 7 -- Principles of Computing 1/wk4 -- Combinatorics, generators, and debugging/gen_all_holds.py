"""
Function to generate permutations of outcomes
Repetition of outcomes not allowed
"""
def get_outcomes(num_die_sides):
    """
    Compute and return a list of possible outcomes (die values) based on the number of sides on a die.
    """
    outcomes = []

    for value in range(1, num_die_sides + 1):
        outcomes.append(value)

    return outcomes


def max_repeats(seq):
    """
    Compute and return the maximum number of times that an outcome is repeated in a sequence.
    """
    # item_count = [seq.count(item) for item in seq]
    # print seq
    # print "item_count:", item_count
    # print "max(item_count):", max(item_count)
    # return max(item_count)
    outcomes = get_outcomes(6)

    max_times = [seq.count(value) for value in outcomes]
    # print "max_times:", max_times
    # print "max value:", max_times.index(max(max_times)) + 1
    return max_times


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """

    # iterate over the entries of hand and compute all possible holds for the first k entries in hand using all possible holds for the first k−1 entries of hand
    ans_set = set([()])
    print "hand:", hand

    for dummy_idx in range(len(hand)):
        print "\ndummy_idx:", dummy_idx

        temp_set = set([()])

        for seq in ans_set:
            print "seq:", seq

            for item in hand:
                print "item:", item

                new_seq = list(seq)
                print "new_seq:", new_seq

                if item not in new_seq or hand.count(item) > 1:
                    new_seq.append(item)
                    print "new_seq:",  new_seq
                    new_seq = sorted(new_seq)
                    print "sorted(new_seq):", new_seq
                temp_set.add(tuple(new_seq))

        ans_set = temp_set
    return ans_set


# Tests
print "gen_all_holds Test #1:"
hand = (2, 4)
print gen_all_holds(hand)
print "Expected: set([(), (2,), (4,), (2, 4)])"

print "\ngen_all_holds Test #2:"
hand = (3, 3, 3)
print gen_all_holds(hand)
print "Expected: set([(), (3,), (3, 3), (3, 3, 3)])"

print "\ngen_all_holds Test #3:"
hand = (1, 2, 2)
print gen_all_holds(hand)
print "Expected: set([(), (1, 2, 2), (1,), (2,), (1, 2), (2, 2)])"


# hand: (2, 4)
# Computed: set([(2, 2), (2, 4), (4, 2), (4, 4)]) 
# Expected: set([(), (2,), (4,), (2, 4)])

# Coding gen_all_holds
# Implementing gen_all_holds is one of the main challenges of this mini - project. While its implementation is short, the actual code requires thought. Since tuples are immutable, your algorithm for computing the required set of tuples cannot directly delete from the tuple hand. Instead, gen_all_holds should compute the set of all possible holds in a manner very similar to that of gen_all_sequences. In particular, your implementation should iterate over the entries of hand and compute all possible holds for the first k entries in hand using all possible holds for the first k−1 entries of hand.