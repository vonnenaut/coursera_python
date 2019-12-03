"""
Student code for Word Wrangler game

Should not use set, sorted, or sort.

Important: None of these functions should mutate their inputs. You must leave the inputs as they are and return new lists.
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided
import poc_simpletest

# REST_STRINGS = []
WORDFILE = "assets_scrabble_words3.txt"

# Functions to manipulate ordered word lists
def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    no_duplicates = []

    for word in list1:
        if no_duplicates.count(word) == 0:
            no_duplicates.append(word)
    return no_duplicates

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    intersection = []
    for word in list1:
        if word in list2:
            intersection.append(word)
    return intersection

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in either list1 or list2.

    This function can be iterative.
    """
    unsorted_merged = list1 + list2
    return merge_sort(unsorted_merged)
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if list1 == []:
        return list1
    else:
        pivot = list1[0]
        lesser = [num for num in list1 if num < pivot]
        pivots = [num for num in list1 if num == pivot]
        greater = [num for num in list1 if num > pivot]
        return merge_sort(lesser) + pivots + merge_sort(greater)

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word in any order.
    Returns a list of all strings that can be formed from the letters in word.  This function should be recursive.   
    # 1. Split the input word into two parts: the first 
    # character (first) and the remaining part (rest).
    # 2. Use gen_all_strings to generate all appropriate 
    # strings for rest. Call this list REST_STRINGS.
    # 3. For each string in REST_STRINGS, generate new strings by 
    # inserting the initial character, first, in all possible 
    # positions within the string.
    # 4. Return a list containing the strings in REST_STRINGS 
    # as well as the new strings generated in step 3.
    """    
    # global REST_STRINGS
    # REST_STRINGS = ['']
    rest_strings = ['']

    # base case
    if len(word) == 1:
        if word not in rest_strings:
            rest_strings.append(word)
        return rest_strings
    # recursive case       
    else:
        # first = word[0]
        # rest = word[1:]
        
        # for enum in gen_all_strings(rest):
        #     for index in range(len(enum)+1):          
        #         new_string = enum[:index] + first + enum[index:]
        #         if len(new_string) <= len(word) and enum.count(first) < word.count(first) and [new_string not in REST_STRINGS or new_string.count(new_string[0]) > 1]:
        #             REST_STRINGS.append(new_string)
        # print "new_strings:", new_strings
        # print "REST_STRINGS:", REST_STRINGS
        # return REST_STRINGS

        for index,value in letter_generator(word):
            rest_strings += [value + enum for enum in gen_all_strings(word[:index] + word[index+1:])]
        return rest_strings

def letter_generator(word):
    """ generator which yields each letter of a word, one at a time.
    """
    for letter in word:
        yield word.index(letter), letter
    
# Function to load words from a file
def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    return []

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()



# Testing
def run_suite(option):
    """
    Some informal testing code
    """
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()    

    def test_remove_duplicates():
        print "--------------------"
        print "\nTesting remove_duplicates:"
        list1 = ["apple", "bacon", "taser", "bacon", "apple", "broom", "bacon"]
        list2 = remove_duplicates(list1)
        suite.run_test(list2, ['apple', 'bacon', 'taser', 'broom'], "Test #1:")

        list1 = ["brains", "screams", "boom", "brains", "brains", "screams"]
        list2 = remove_duplicates(list1)
        suite.run_test(list2, ['brains', 'screams', 'boom'], "Test #2:")

    def test_intersect():
        print "--------------------"
        print "\nTesting intersect:"
        list1 = ["Trump", "Vietnam", "The Black Keys", "tube amp"]
        list2 = ["tube amp", "The Black Keys", "rain", "May"]
        inter = intersect(list1, list2)
        suite.run_test(inter, ['The Black Keys', 'tube amp'], "Test #3:") 

        list1 = ["red", "blue", "green"]
        list2 = ["white", "orange", "green"]
        inter = intersect(list1, list2)
        suite.run_test(inter, ['green'], "Test #4:")   

    def test_merge():
        print "--------------------"
        print "\nTesting merge:"
        list1 = ["apple"]
        list2 = ["zebra"]
        merged_list = merge(list1, list2)
        suite.run_test(merged_list, ['apple', 'zebra'], "Test #5:")

        list1 = ["boat"]
        list2 = ["accident"]
        merged_list = merge(list1, list2)
        suite.run_test(merged_list, ['accident', 'boat'], "Test #6:")

        list1 = ["apple", "boat"]
        list2 = ["zebra"]
        merged_list = merge(list1, list2)
        suite.run_test(merged_list, ['apple', 'boat','zebra'], "Test #7:")

        list1 = ["apple", "cloud"]
        list2 = ["boat"]
        merged_list = merge(list1, list2)
        suite.run_test(merged_list, ['apple', 'boat', 'cloud'], "Test #8:")

        list1 = ["shore", "tugboat"]
        list2 = ["anchor"]
        merged_list = merge(list1, list2)
        suite.run_test(merged_list, ['anchor', 'shore', 'tugboat'], "Test #9:")

        list1 = ["apple"]
        list2 = ["boat", "fog"]
        merged_list = merge(list1, list2)
        suite.run_test(merged_list, ['apple', 'boat', 'fog'], "Test #10:")

        list1 = ["cloud"]
        list2 = ["boat", "fog"]
        merged_list = merge(list1, list2)
        suite.run_test(merged_list, ['boat', 'cloud', 'fog'], "Test #11:")

        list1 = ["sail"]
        list2 = ["boat", "fog"]
        merged_list = merge(list1, list2)
        suite.run_test(merged_list, ['boat', 'fog', 'sail'], "Test #12:")

        list1 = ["dark", "fog"]
        list2 = ["cloud", "crow"]
        merged_list = merge(list1, list2)
        suite.run_test(merged_list, ['cloud', 'crow', 'dark', 'fog'], "Test #13:")

        list1 = ["apple", "dredge"]
        list2 = ["boat", "cloud"]
        merged_list = merge(list1, list2)
        suite.run_test(merged_list, ['apple', 'boat', 'cloud', 'dredge'], "Test #14:")

        list1 = ["apple", "boat"]
        list2 = ["dredge", "shoreline"]
        merged_list = merge(list1, list2)
        suite.run_test(merged_list, ['apple', 'boat', 'dredge', 'shoreline'], "Test #15:")

        list1 = ["alight", "dredge"]
        list2 = ["cloud", "shoreline"]
        merged_list = merge(list1, list2)
        suite.run_test(merged_list, ['alight', 'cloud', 'dredge', 'shoreline'], "Test #16:")

        list1 = ["anchor", "dredge"]
        list2 = ["alight", "cloud"]
        merged_list = merge(list1, list2)
        suite.run_test(merged_list, ['alight', 'anchor', 'cloud', 'dredge'], "Test #17:")

        list1 = ["anchor", "dredge"]
        list2 = ["bridge", "lighthouse"]
        merged_list = merge(list1, list2)
        suite.run_test(merged_list, ['anchor', 'bridge', 'dredge', 'lighthouse'], "Test #18:")

        list1 = ["capsized", "riptide"]
        list2 = ["alight", "thunderstorm"]
        merged_list = merge(list1, list2)
        suite.run_test(merged_list, ['alight', 'capsized', 'riptide', 'thunderstorm'], "Test #19:")

    def test_gen_all_strings():
        global REST_STRINGS
        print "--------------------"
        print "\nTesting gen_all_strings:"
        REST_STRINGS = []
        word = "a"
        unfiltered_result = gen_all_strings(word)
        suite.run_test(gen_all_strings(word), ['', 'a'], "Test #20:")

        REST_STRINGS = []
        word = "ok"        
        unfiltered_result = gen_all_strings(word)
        suite.run_test(gen_all_strings(word), ['', 'o', 'ok', 'k', 'ko'], "Test #21:")

        REST_STRINGS = []
        word = "bin"    
        unfiltered_result = gen_all_strings(word)
        suite.run_test(gen_all_strings(word), ['', 'b', 'bi', 'bin', 'bn', 'bni', 'i', 'ib', 'ibn', 'in', 'inb', 'n', 'nb', 'nbi', 'ni', 'nib'], "Test #22:")

        REST_STRINGS = []
        word = "aa"        
        unfiltered_result = gen_all_strings(word)
        suite.run_test(gen_all_strings(word), ['', 'a', 'aa', 'aa'], "Test #23:")
        
    def test_all():
        print "-------------------"
        print "\nRunning all tests:"
        test_remove_duplicates()
        test_intersect()
        test_merge()
        test_gen_all_strings()

    test_choices = {1: test_all,
                    2: test_remove_duplicates,
                    3: test_intersect,
                    4: test_merge,
                    5: test_gen_all_strings}

    try:
        test_choices[option]()
    except KeyError, e:
        print "KeyError %s" % str(e)
    
    suite.report_results()

# Testing options:
# 1: test_all
# 2: test_remove_duplicates
# 3: test_intersect
# 4: test_merge
# 5: test_gen_all_strings

run_suite(1) 
    