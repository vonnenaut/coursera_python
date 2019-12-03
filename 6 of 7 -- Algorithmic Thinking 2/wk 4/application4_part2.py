"""
Provide code and solution for Application 4
"""

DESKTOP = True

import math
import random
import urllib2

if DESKTOP:
    import matplotlib.pyplot as plt
    import application4 as student
else:
    import simpleplot
    import userXX_XXXXXXX as student
    

# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"



###############################################
# provided code

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.  

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib2.urlopen(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict




def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = urllib2.urlopen(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urllib2.urlopen(filename)
    
    # read in files as string
    words = word_file.read()
    
    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list


def question1():
    # load protein sequences and scoring matrix
    human_ep = read_protein(HUMAN_EYELESS_URL)
    fruitfly_ep = read_protein(FRUITFLY_EYELESS_URL)
    scoring_matrix = read_scoring_matrix(PAM50_URL)

    # compute local alignments
    alignment_matrix = student.compute_alignment_matrix(human_ep, fruitfly_ep, scoring_matrix, False)
    print student.compute_local_alignment(human_ep, fruitfly_ep, scoring_matrix, alignment_matrix)

def question2():
    # remove dashes from sequences computed in question 1
    seq1 = 'HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEKQQ'
    seq2 = 'HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATAEVVSKISQYKRECPSIFAWEIRDRLLQENVCTNDNIPSVSSINRVLRNLAAQKEQQ'
    pax = read_protein(CONSENSUS_PAX_URL)
    scoring_matrix = read_scoring_matrix(PAM50_URL)

    # compute global alignment of each sequence with the pax sequence
    alignment_matrix_1 = student.compute_alignment_matrix(seq1, pax, scoring_matrix, True)
    ga_seq1 = student.compute_global_alignment(seq1, pax, scoring_matrix, alignment_matrix_1)
    alignment_matrix_2 = student.compute_alignment_matrix(seq2, pax, scoring_matrix, True)
    ga_seq2 = student.compute_global_alignment(seq1, pax, scoring_matrix, alignment_matrix_2)

    # print "ga_seq1:", ga_seq1
    # print "ga_seq2:", ga_seq2

    # Compare corresponding elements of these two globally-aligned sequences (local vs. consensus) and compute the percentage of elements in these two sequences that agree.
    score = 0
    for letter1, letter2 in zip(ga_seq1[1], ga_seq2[1]):
        # print "letter1:", letter1, "letter2:", letter2
        if letter1 == letter2:
            score += 1
    percentage1 = score / float(len(ga_seq1[1]))
    percentage2 = score / float(len(ga_seq2[1]))
    print "score:", score
    print "len(ga_seq1[1]):", len(ga_seq1[1])
    print "len(ga_seq2[1]):", len(ga_seq2[1])
    print "percentage1:", percentage1
    print "percentage2:", percentage2



# question1()
# (875, 'HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEK-QQ', 'HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATAEVVSKISQYKRECPSIFAWEIRDRLLQENVCTNDNIPSVSSINRVLRNLAAQKEQQ')

# question2()
# score: 17
# percentage1: 0.127819548872
# percentage2: 0.123188405797


# Question 3 (1 pt)
# Examine your answers to Questions 1 and 2. Is it likely that the level of similarity exhibited by the answers could have been due to chance? In particular, if you were comparing two random sequences of amino acids of length similar to that of HumanEyelessProtein and FruitflyEyelessProtein, would the level of agreement in these answers be likely? To help you in your analysis, there are 23 amino acids with symbols in the string ("ACBEDGFIHKMLNQPSRTWVYXZ"). Include a short justification for your answer.
# No.  Justification:  Probability of event of randomly getting 17 matching letters out of 23 possible with a sequence length of 133 and 138 respectively:
# seq1:  (1/23)*17 / 133 = 0.0055573716900948 which is far less than 0.127819548872
# seq2:  (1/23)*17 / 138 = 0.0053560176433522 which is far less than 0.123188405797











