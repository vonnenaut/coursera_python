"""
Function to generate permutations of outcomes
Repetition of outcomes not allowed
"""
NUM_DIE_SIDES = 6


def get_outcomes(num_die_sides):
    """
    Compute and return a list of possible outcomes (die values) based on the number of sides on a die.
    """
    outcomes = []
    for value in range(1, num_die_sides + 1):
        outcomes.append(value)
    return outcomes


def get_quantities(seq):
    """
    Compute and return the number of times that all items in a sequence are repeated.

    Returns a list numbering quantity with index+1 equal to the value represented by that quantity.
    """
    outcomes = get_outcomes(NUM_DIE_SIDES)
    quants = [seq.count(value) for value in outcomes]
    return quants


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """

    # iterate over the entries of hand and compute all possible holds for the
    # first k entries in hand using all possible holds for the first k−1
    # entries of hand
    ans_set = set([()])
    hand_quants = quantities(hand)
    # print "quants:", quants
    print "hand:", hand

    for dummy_idx in range(len(hand)):
        print "\n\ndummy_idx:", dummy_idx

        temp_set = set([()])

        for seq in ans_set:
            # print "seq:", seq

            for item in hand:
                print "\nitem:", item

                new_seq = list(seq)
                print "new_seq:", new_seq
                print "hand.count(item):", hand.count(item)
                print "new_seq.count(item):", new_seq.count(item)

                if hand.count(item) > new_seq.count(item):
                    new_seq.append(item)
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
print "hand:", hand

print "\ngen_all_holds Test #2:"
hand = (3, 3, 3)
print gen_all_holds(hand)
print "Expected: set([(), (3,), (3, 3), (3, 3, 3)])"
print "hand:", hand

print "\ngen_all_holds Test #3:"
hand = (1, 2, 2)
print gen_all_holds(hand)
print "Expected: set([(), (1, 2, 2), (1,), (2,), (1, 2), (2, 2)])"
print "hand:", hand

# hand: (2, 4)
# Computed: set([(2, 2), (2, 4), (4, 2), (4, 4)])
# Expected: set([(), (2,), (4,), (2, 4)])

# Coding gen_all_holds
# Implementing gen_all_holds is one of the main challenges of this mini -
# project. While its implementation is short, the actual code requires
# thought. Since tuples are immutable, your algorithm for computing the
# required set of tuples cannot directly delete from the tuple hand.
# Instead, gen_all_holds should compute the set of all possible holds in a
# manner very similar to that of gen_all_sequences. In particular, your
# implementation should iterate over the entries of hand and compute all
# possible holds for the first k entries in hand using all possible holds
# for the first k−1 entries of hand.
