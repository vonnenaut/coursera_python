# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors
# http://www.codeskulptor.org/#user42_qgI79zP0ZgDz762.py

from random import randrange


# helper functions

def name_to_number(name):
    # delete the following pass statement and fill in your code below
    # pass

    # convert name to number using if/elif/else
    # don't forget to return the result!
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    else:
        return "Improper name given.  Cannot convert to a number."

def number_to_name(number):
    # delete the following pass statement and fill in your code below
    # pass
    
    # convert number to a name using if/elif/else
    # don't forget to return the result!
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
    else:
        return "Improper number given.  Cannot convert to a name."

def rpsls(player_choice): 
    # delete the following pass statement and fill in your code below
    # pass
    
    # print a blank line to separate consecutive games
    print "\n"
    
    # print out the message for the player's choice
    print "Player chooses %s" % (player_choice)
    
    # convert the player's choice to player_number using the function name_to_number()
    player_num = name_to_number(player_choice)
    
    # compute random guess for comp_number using random.randrange()
    comp_num = randrange(0, 5)
    
    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_num)
    
    # print out the message for computer's choice
    print "Computer chooses %s" % (comp_choice)

    # compute difference of comp_number and player_number modulo five
    diff_mod = (comp_num - player_num) % 5
    
    # use if/elif/else to determine winner, print winner message
    if diff_mod == 3 or diff_mod == 4:
        print "Player wins!"
    elif diff_mod == 1 or diff_mod == 2:
        print "Computer wins!"
    else:
    	print "Player and computer tie!"
    
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric


