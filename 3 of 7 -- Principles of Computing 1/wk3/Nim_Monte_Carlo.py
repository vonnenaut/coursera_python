""" 
Coursera -- Foundations in Computing 3 of 7
Principles of Computing 1 Week 3
Practice Mini-project:  Nim (Monte Carlo) aka 21
Daniel Ashcom
03/26/17

A simple Monte Carlo solver for Nim
http://en.wikipedia.org/wiki/Nim#The_21_game
"""

import random
import codeskulptor
codeskulptor.set_timeout(20)

MAX_REMOVE = 3
TRIALS = 10000

def evaluate_position(num_items):
    """
    Monte Carlo evalation method for Nim ---
    uses a Monte Carlo simulation to compute a good move for a given number of items in the heap. """
    comp_wins = 0
    player_wins = 0

    initial_move = random.randrange(MAX_REMOVE + 1)
    num_items -= initial_move
    next_move = random.randrange(MAX_REMOVE + 1)
    





    
    
    return 0


def play_game(start_items):
    """
    Play game of Nim against Monte Carlo bot
    """
    
    current_items = start_items
    print "Starting game with value", current_items
    while True:
        comp_move = evaluate_position(current_items)
        current_items -= comp_move
        print "Computer choose", comp_move, ", current value is", current_items
        if current_items <= 0:
            print "Computer wins"
            break
        player_move = int(input("Enter your current move"))
        current_items -= player_move
        print "Player choose", player_move, ", current value is", current_items
        if current_items <= 0:
            print "Player wins"
            break

# play_game(21)
play_game(6)
        
    
                 
    