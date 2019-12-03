def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    DO NOT MODIFY.

    outcomes:  possible values of a roll (ex. -- [1,2,3,4,5,6] for a 6-sided die)
    """
    # iterates over the entries of hand and computes all possible holds for
    # the first k entries in hand using all possible holds for the first k−1
    # entries of hand

    # Combinations:  As was the case when repetition was allowed, the order of
    # the resulting sequence may not matter in some applications.  The
    # standard technique for handling this situation is to group all sequences
    # that correspond to the same set of outcomes in a single cluster. (Note
    # we can use a set here instead of a sorted sequence since repetition is
    # not allowed.)
    ans = set([()])

    for dummy_idx in range(length):
        temp = set([()])
        for seq in ans:
            for item in outcomes:
                new_seq = list(seq)
                if item not in new_seq:
                    new_seq.append(item)
                temp_set.add(tuple(new_seq))
        ans = temp
    return ans


# outcomes = (3, 3, 3)
outcomes = (2, 4)
print gen_all_sequences(outcomes, len(outcomes))
