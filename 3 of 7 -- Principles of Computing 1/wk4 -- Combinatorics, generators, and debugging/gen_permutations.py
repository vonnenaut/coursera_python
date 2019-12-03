"""
Function to generate permutations of outcomes
Repetition of outcomes not allowed
"""


def gen_permutations(outcomes, length):
    """
    Iterative function that generates set of permutations of
    outcomes of length num_trials
    No repeated outcomes allowed
    """
    ans = set([()])
    for dummy_idx in range(length):
        temp = set([()])
        for seq in ans:
            for item in outcomes:
                new_seq = list(seq)
                new_seq.append(item)
                if tuple(new_seq) not in temp:
                    temp.add(tuple(new_seq))
        ans = temp
    return ans

outcomes = (3, 3, 3)
# outcomes = (2, 4)
print gen_permutations(outcomes, len(outcomes))

# Coding gen_all_holds
# Implementing gen_all_holds is one of the main challenges of this mini - project. While its implementation is short, the actual code requires thought. Since tuples are immutable, your algorithm for computing the required set of tuples cannot directly delete from the tuple hand. Instead, gen_all_holds should compute the set of all possible holds in a manner very similar to that of gen_all_sequences. In particular, your implementation should iterate over the entries of hand and compute all possible holds for the first k entries in hand using all possible holds for the first k−1 entries of hand.