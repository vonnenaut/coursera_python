# Rock-paper-scissors-lizard-Spock

# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

## Rules ###############
# scissors cuts paper     paper covers rock
# rock crushes lizard     lizard poisons Spock
# Spock smashes scissors  scissors decapitates lizard
# lizard eats paper       paper disproves Spock
# Spock vaporizes rock    rock crushes scissors


#imports
import random


# helper functions
def number_to_name(number):    
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
    else:
        return "scissors"
    

def name_to_number(name):
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
    else:
        return 4


def rpsls(player_choice): 
    
    # print a blank line to separate consecutive games
    print()
    
    # print out the message for the player's choice
    print("Player chooses", player_choice)

    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)
    # print("player_number: ", player_number)

    # compute random guess for comp_number using random.randrange()
    # comp_number = 0
    comp_number = random.randrange(5)
    

    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)
    # print("comp_choice: ", comp_choice)
    
    # print out message for computer's choice
    print("Computer chooses", comp_choice)

    # compute difference of player_number and comp_number modulo five
    difference = (comp_number - player_number) % 5
    # print("difference: ", difference)

    # use if/elif/else to determine winner and print winner message
    if difference == 0:
        print("Player and computer tie!")
    elif (difference == 1) or (difference == 2):
        print("Computer wins!")
    else:
        print("Player wins!") 
    


# test your code
for idx in range(5):
    inputs = ["rock", "paper", "scissors", "lizard", "Spock"]
    for input in inputs:
        rpsls(input)

# Error-tracking:
# Player chooses scissors Computer chooses rock Player wins! 
# Should be 'Computer wins'

# Player chooses lizard Computer chooses rock Player wins!
# Should be 'Computer wins'

# print(number_to_name(0)) # rock
# print(number_to_name(1)) # Spock
# print(number_to_name(2)) # paper
# print(number_to_name(3)) # lizard
# print(number_to_name(4)) # scissors

# print(name_to_number('scissors')) # 4
# print(name_to_number('rock')) # 0
# print(name_to_number('lizard')) # 3
# print(name_to_number('paper')) # 2
# print(name_to_number('Spock')) # 1

# rpsls('scissors') # Computer wins
# rpsls('lizard') # Computer wins