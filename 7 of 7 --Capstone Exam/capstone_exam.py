""" 
Coursera Fundamentals of Computing 
Capstone Exam
"""
# ------------------------------------------------
# Question 5
class BankAccount:
    def __init__(self, initial_balance):
        """
        Creates an account with the given balance.
        """
        self.balance = initial_balance
        self.fees = 0

    def deposit(self, amount):
        """
        Deposits the amount into the account.
        """
        self.balance += amount

    def withdraw(self, amount):
        """
        Withdraws the amount from the account.  
        Each withdrawal resulting in a balance of 
        less than 10 dollars (before any fees) also 
        deducts a penalty fee of 5 dollars from the balance.
        """
        self.balance -= amount
        if self.balance < 10:
                self.balance -= 5
                self.fees += 5

    def get_balance(self):
        """
        Returns the current balance in the account.
        """
        return self.balance

    def get_fees(self):
        """
        Returns the total fees ever deducted from the account.
        """
        return self.fees


def test_BankAccount():
    """Tests BankAccount class """
    account1 = BankAccount(10)
    account1.withdraw(15)
    account2 = BankAccount(15)
    account2.deposit(10)
    account1.deposit(20)
    account2.withdraw(20)
    print account1.get_balance(), account1.get_fees(), account2.get_balance(), account2.get_fees()

# Question 5 test
def q5():
    account1 = BankAccount(20)
    account1.deposit(10)
    account2 = BankAccount(10)
    account2.deposit(10)
    account2.withdraw(50)
    account1.withdraw(15)
    account1.withdraw(10)
    account2.deposit(30)
    account2.withdraw(15)
    account1.deposit(5)
    account1.withdraw(20)
    account2.withdraw(15)
    account2.deposit(25)
    account2.withdraw(15)
    account1.deposit(10)
    account1.withdraw(50)
    account2.deposit(25)
    account2.deposit(25)
    account1.deposit(30)
    account2.deposit(10)
    account1.withdraw(15)
    account2.withdraw(10)
    account1.withdraw(10)
    account2.deposit(15)
    account2.deposit(10)
    account2.withdraw(15)
    account1.deposit(15)
    account1.withdraw(20)
    account2.withdraw(10)
    account2.deposit(5)
    account2.withdraw(10)
    account1.deposit(10)
    account1.deposit(20)
    account2.withdraw(10)
    account2.deposit(5)
    account1.withdraw(15)
    account1.withdraw(20)
    account1.deposit(5)
    account2.deposit(10)
    account2.deposit(15)
    account2.deposit(20)
    account1.withdraw(15)
    account2.deposit(10)
    account1.deposit(25)
    account1.deposit(15)
    account1.deposit(10)
    account1.withdraw(10)
    account1.deposit(10)
    account2.deposit(20)
    account2.withdraw(15)
    account1.withdraw(20)
    account1.deposit(5)
    account1.deposit(10)
    account2.withdraw(20)
    print account1.get_balance(), account1.get_fees(), account2.get_balance(), account2.get_fees()

# should return 10 5 0 5
test_BankAccount()

# question 5
q5()


# -----------------------------------------------------------
# Question 7
# Rock-paper-scissors-lizard-Spock template

import random

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

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
    print
    
    # print out the message for the player's choice
    print "Player chooses", player_choice

    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)

    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(5)

    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)
    
    # print out message for computer's choice
    print "Computer chooses", comp_choice

    # compute difference of player_number and comp_number modulo five
    difference = comp_number - player_number % 5

    # use if/elif/else to determine winner and print winner message
    if difference == 0:
        print "Player and computer tie!"
    elif (difference == 1) or (difference == 2):
        print "Computer wins!"
    else:
        print "Player wins!"
        
    

     
    
# test your code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric