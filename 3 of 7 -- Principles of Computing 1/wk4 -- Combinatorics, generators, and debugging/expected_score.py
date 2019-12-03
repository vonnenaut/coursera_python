import poc_simpletest

NUM_DICE = 5
NUM_DIE_SIDES = 6

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
        "arg is an empty sequence"
    return max_item


def get_quantities(seq):
    """
    Compute and return the number of times that all items in a sequence are repeated.

    Returns a list numbering quantity with index+1 equal to the value represented by that quantity.
    """
    outcomes = get_outcomes(NUM_DIE_SIDES)
    quants = [seq.count(value) for value in outcomes]
    return quants


def get_outcomes(num_die_sides):
    """
    Compute and return a list of possible outcomes (die values) based on the number of sides on a die.
    """
    outcomes = []

    for value in range(1, num_die_sides + 1):
        outcomes.append(value)

    return outcomes


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
    # print "hand:", hand
    score = 0
    quants = get_quantities(hand)
    idx = -1
    matches = False

    for quant in quants:
        if quant > 1:
            matches = True

    # print "matches:", matches

    if matches:
        for quant in quants:
            idx += 1
            if quant > 1:
                score += (idx + 1) * quants[idx]
                # print "idx1:", idx
        return score

    elif not matches:
        for quant in quants:
            idx += 1
            score += (idx + 1) * quants[idx]
            # print "idx2:", idx
        return score


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
    print "outcomes:", outcomes

    # generate all possible sequences of rolls
    all_rolls = list(gen_all_sequences(outcomes, num_free_dice))
    results = [max_repeats(roll) for roll in all_rolls]
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
    best_score = 0
    dice_to_hold = []

    for hold in possible_holds:
        hold_val = expected_value(hold, NUM_DIE_SIDES, NUM_DICE - len(hold))

        hand_score = score(hold) + score(hand)
        if hand_score > best_val:
            # best_val = hold_val
            best_score = hand_score
            dice_to_hold = hold
    hand_copy = list(hand)
    sugg_hand = hand_copy.append(dice_to_hold)
    return (hand_score, sugg_hand)


def run_example():
    """
    Testing suite
    """
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()

    # OwlTest Troubleshooting:
    print "\n\n-----score test #2-----:"
    hand = (4, 5)
    suite.run_test(score(hand), 5, "Test #1:")

    print "\n\n-----expected_value test #6-----"
    suite.run_test(expected_value((2, 2), 6, 2), 5.83333333333, "Test #2:")

run_example()
