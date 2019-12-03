"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level

A strategy function designed to help you choose which dice to hold after your second roll during the first turn of a game of Yahtzee. This function will consider all possible choices of dice to hold and recommend the choice that maximizes the expected value of your score after the final roll.

"""

# Used to increase the timeout, if necessary
import codeskulptor
import math
# import poc_simpletest

NUM_DICE = 5
NUM_DIE_SIDES = 6


codeskulptor.set_timeout(20)


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
    max_item = 0
    item_count = [seq.count(item) for item in seq]
    try:
        max_item = max(item_count)
    except ValueError:
        print "arg is an empty sequence"
    return max_item


def get_quantities(seq):
    """
    Compute and return the number of times that all items in a sequence are repeated.

    Returns a list numbering quantity with index+1 equal to the value represented by that quantity.
    """
    outcomes = get_outcomes(NUM_DIE_SIDES)
    quants = [seq.count(value) for value in outcomes]
    return quants


def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    DO NOT MODIFY.

    outcomes:  possible values of a roll (ex. -- [1,2,3,4,5,6] for a 6-sided die)
    """

    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score
    """
    max_value = max(hand)
    scores = [0 for dummy_idx in range(max_value)]

    for die in hand:
        scores[die - 1] += die

    return max(scores)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes = get_outcomes(num_die_sides)
    # print "outcomes:", outcomes

    # generate all possible sequences of rolls
    all_rolls = gen_all_sequences(outcomes, num_free_dice)
    value = 0.0

    for result in all_rolls:
        curr_hand = tuple(list(held_dice) + list(result))
        value += score(curr_hand)

    return value / len(all_rolls)


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    ans_set = set([()])

    for dummy_idx in range(len(hand)):
        temp_set = set([()])
        for seq in ans_set:
            for item in hand:
                new_seq = list(seq)
                if hand.count(item) > new_seq.count(item):
                    new_seq.append(item)
                    new_seq = sorted(new_seq)
                temp_set.add(tuple(new_seq))
        ans_set = temp_set
    return ans_set


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """

    possible_holds = gen_all_holds(hand)
    best_val = 0
    dice_to_hold = ()
    for hold in possible_holds:
        hold_val = expected_value(hold, NUM_DIE_SIDES, len(hand) - len(hold))
        
        if hold_val > best_val:
            best_val = hold_val
            dice_to_hold = hold

    return (best_val, dice_to_hold)


# def run_example():
#     """
#     Testing suite
#     """
#     # create a TestSuite object
#     suite = poc_simpletest.TestSuite()

#     # OwlTest Troubleshooting:
#     print "\n\n-----expected_value test #6-----"
#     suite.run_test(expected_value((2, 2), 6, 2), 5.83333333333, "Test #8:")

#     print "\n\n-----score test #2-----:"
#     hand = (4, 5)
#     suite.run_test(score(hand), 5, "Test #9:")

#     print "\n\n-----strategy test #4-----:"
#     suite.run_test(strategy((1,), 6), (3.5, ()), "Test #10:")

#     suite.run_test(strategy((1, 2, 3, 3, 4), 4),  (8.53125, (3, 3)), "Test #11:")

#     print "\n"
#     suite.report_results()


# run_example()
