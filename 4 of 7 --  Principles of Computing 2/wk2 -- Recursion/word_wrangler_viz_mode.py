"""
Student code for Word Wrangler game

Should not use set, sorted, or sort.

Important: None of these functions should mutate their inputs. You must leave the inputs as they are and return new lists.
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided
import poc_simpletest

WORDFILE = "assets_scrabble_words3.txt"
rest_strings = []


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
    * Consider using zip to simplify this method.
    zip can iterate over two lists at the same time.
    """   
    merged_list = []
    print "list1:", list1
    print "list2:", list2
    
    if len(list1) == 1 and len(list2) == 1:
        if list1[0] < list2[0]:
            return list1 + list2
        else:
            return list2 + list1
    elif len(list1) > 1 and len(list2) == 1:
        for element in list1:
            if list2[0] < element:
                copy_list1 = list1[:]
                return copy_list1[:copy_list1.index(element)] + list2 + copy_list1[copy_list1.index(element):]
        return list1 + list2
    elif len(list1) == 1 and len(list2) > 1:
        for element in list2:
            if list1[0] < element:
                copy_list2 = list2[:]
                return copy_list2[:copy_list2.index(element)] + list1 + copy_list2[copy_list2.index(element):]
        return list2 + list1
    else: # both list1 and list2 lengths are > 1
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
    """

    # This is a rough outline of one approach that will allow you to generate all strings that can be composed from the letters of word. (Remember to think about the base case!)
    global rest_strings

    print "word:", word
    
    # base cases
    if word == "":
        return [""]
    elif len(word) is 1:
        return ["", word]
    else:   # recursive case       
        # 1. Split the input word into two parts: the first character (first) and 
        # the remaining part (rest).
        first = word[0]
        rest = word[1:]
        # 2. Use gen_all_strings to generate all appropriate strings for rest. 
        # Call this list rest_strings.
        rest_strings.append(gen_all_strings(rest))
        print "rest_strings", rest_strings

        # 3. For each string in rest_strings, generate new strings by inserting 
        # the initial character, first, in all possible positions within the string.
        new_strings = []
        for string in rest_strings:
            for index in range(len(string)):
                new_strings.append(string[:index] + list(first) + string[index:])
            rest_strings.append(new_strings)

        # 4. Return a list containing the strings in rest_strings as well as the new 
        # strings generated in step 3.
        return rest_strings
        

        # new_strings = []
        # for index in range(len(rest)):
        #     new_strings += rest[:index] + first + rest[index:]
        # for string in new_strings:
        #     if 
        #     rest_strings += gen_all_strings(string)
        # return rest_strings

    
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
# print gen_all_strings("a")
print gen_all_strings("ok")    
    