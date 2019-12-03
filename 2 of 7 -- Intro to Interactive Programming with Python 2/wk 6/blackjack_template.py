# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
deck = []

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        """ creates Hand object """
        self.hand = [] # an empty list for Card objects constituting a hand

    def __str__(self):
        """ returns a string representation of a hand """
        string = "Hand contains "
        h = self.hand
        
        for i in range(len(h)):
            string += str(h[i].get_suit()) + str(h[i].get_rank()) + " "
        
        return string

    def add_card(self, card):
        """ adds a card object to a hand """
        self.hand.append(card)

    def get_value(self):
        """ computes the value of the hand, see Blackjack video counts aces as 1, if the hand has an ace, then adds 10 to hand value if it doesn't bust """
        global VALUES
        hand_value = 0
        has_ace = False

        # This works but it seems awfully wordy...  how to be more concise?
        for card in self.hand:
            if card.get_rank() is 'A':
                has_ace = True

        if has_ace is False:
            for i in self.hand:
                v = VALUES[i.get_rank()]
                hand_value += v
            return hand_value
        else:
            for i in self.hand:
                v = VALUES[i.get_rank()]
                hand_value += v
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                for i in self.hand:
                    v = VALUES[i.get_rank()]
                    hand_value += v
                return hand_value

   
    def draw(self, canvas, pos):
        pass    # draw a hand on the canvas, use the draw method for cards
 
        
# define deck class 
class Deck:
    def __init__(self):
        """ creates a Deck object """
        self.deck = []

        for i in SUITS:
            for j in RANKS:
                self.deck.append(Card(i, j))

        
    def shuffle(self):
        """ shuffles the deck """
        random.shuffle(self.deck)

    def deal_card(self):
        """ deals a card object from the deck """
        return self.deck.pop()
    
    def __str__(self):
        """ returns a string representing the deck """
        string = "Deck contains "

        for i in range(len(self.deck)):
            string += str(self.deck[i].get_suit()) + str(self.deck[i].get_rank()) + " "
        return string



#define event handlers for buttons
def deal():
    global outcome, in_play, deck

    # creat a Deck object and shuffle all the cards
    deck = Deck()
    deck.shuffle()
    # create a player hand, adding two cards from the deck
    player_hand = Hand()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    # create a dealer hand, adding two cards from the deck
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

    print "Dealer hand: ", dealer_hand
    print "Dealer hand value: ", dealer_hand.get_value()
    print "Player hand: ", player_hand
    print "Player hand value: ", player_hand.get_value()
    
    in_play = True

def hit():
    pass    # replace with your code below
 
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    pass    # replace with your code below
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    card = Card("S", "A")
    card.draw(canvas, [300, 300])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric