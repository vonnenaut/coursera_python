# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 950x392
card_size = (73, 98)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

card_back_size = (71, 96)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize global variables
deck = []
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ['C', 'S', 'H', 'D']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (card_size[0] * (0.5 + RANKS.index(self.rank)), card_size[1] * (0.5 + SUITS.index(self.suit)))
        canvas.draw_image(card_images, card_loc, card_size, [pos[0] + card_size[0] / 2, pos[1] + card_size[1] / 2], card_size)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.has_ace = False

    def __str__(self):
        return str([str(c) for c in self.cards])

    def add_card(self, card):
        self.cards.append(card)
        self.value += VALUES[card.get_rank()] # Line 59: AttributeError: 'tuple' object has no attribute 'get_rank'
        if card.get_rank() == 'A':
            self.has_ace = True

    # count aces as 1, if the hand has an ace, then add 10 to hand value if don't bust
    def get_value(self):
        if self.has_ace and self.value <= 11:
            return self.value + 10
        else:
            return self.value

    def busted(self):
        return self.value > 21
    
    def draw(self, canvas, p):
        for i in range(len(self.cards)):
            (self.cards[i]).draw(canvas, (p[0] + 100 * i, p[1]))

# define deck class
class Deck:
    def __init__(self):
        self.restore()

    def restore(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append((suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()


#define callbacks for buttons
def deal():
    global deck, p_hand, d_hand, in_play, outcome
    
    # initialize and shuffle deck, could use random.shuffle()
    deck = Deck()
    deck.shuffle()
        
    # deal out hands
    d_hand = Hand()
    p_hand = Hand()
    d_hand.add_card(deck.deal_card())
    p_hand.add_card(deck.deal_card())
    d_hand.add_card(deck.deal_card())
    p_hand.add_card(deck.deal_card())
    outcome = ""
    in_play = True

def hit():
    global in_play, outcome, score
    if not(in_play):
        return
    p_hand.add_card(deck.deal_card())
    if p_hand.busted():
        outcome = "You went bust and lose. "
        in_play = False
        score -= 1
        
def stand():
    global outcome, in_play, score
    if not(in_play):
        return    	
    while d_hand.get_value() < 17:
        d_hand.add_card(deck.deal_card())
    if p_hand.get_value() <= d_hand.get_value() and not(d_hand.busted()):
        outcome = "You lose."
        score -= 1
    else:
        outcome = "You win."
        score += 1
    in_play = False

def draw(canvas):
    canvas.draw_text("Blackjack", (100, 100), 36, "Aqua")
    canvas.draw_text("Score " + str(score), (400, 100), 24, "Black")
    canvas.draw_text("Dealer", (75, 170), 24, "Black")
    canvas.draw_text("Player", (75, 370), 24, "Black")
    canvas.draw_text(outcome, (225, 170), 24, "Black")
    d_hand.draw(canvas, (75, 200))
    p_hand.draw(canvas, (75, 400))
    if in_play:
        canvas.draw_image(card_back, [35, 48], card_back_size, [112, 249], card_back_size)
        canvas.draw_text("Hit or stand?", (225, 370), 24, "Black")
    else:
        canvas.draw_text("New deal?", (225, 370), 24, "Black")    


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# deal an initial hand
deal()

# get things rolling
frame.start()
