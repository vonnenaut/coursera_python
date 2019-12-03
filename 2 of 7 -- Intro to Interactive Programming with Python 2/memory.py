# implementation of card game - Memory

import simplegui
import random

# globals
##
set1 = range(1,9)
set2 = range(1,9)
deck = []			# int, values of card-faces for combined set1 and set1
exposed = []		# boolean, keeps track of which cards are showing (picked or matched)
game_state = 0		# int, game_state of game:
                        # 0:  beginning of game
                        # 1:  1 card has been picked/shown
                        # 2:  2 cards have been picked/shown
c1_index = 0		# index of first card picked
c2_index = 0		# index of second card picked
turn = 1 				# game turn


# helper function to initialize globals
##
def new_game():
    """ sets up the deck for a new game """
    # globals accessed by new_game()
    global set1, set2, deck, exposed, turn, c1_index, c2_index, game_state
    
    # reset the turn counter and matched pairs
    turn = 1
       
    # update label
    label.set_text("Turns = %s" % str(turn))
    
    # reset indexes and game state
    c1_index = 0
    c2_index = 0
    game_state = 0
    
    # set up the deck
    deck = []
    random.shuffle(set1)
    random.shuffle(set2)
    deck.extend(set1)
    deck.extend(set2)
    random.shuffle(deck)    
    
    # set all cards initially to hidden/unexposed
    exposed = [False] * 16
        
    
# event handlers
##
def mouseclick(pos):
    """ handles mouse clicks and the logic of the game """
    # globals accessed by mouseclick(pos)
    global game_state, exposed, c1_index, c2_index, deck, turn
    
    # determine index of clicked card
    index = pos[0] // 50

    if exposed[index] is False:  # if clicked card is hidden
    # Game state 0: if no cards are face-up, on click, do the following:
    	if game_state == 0:        
        	exposed[index] = True	# unhide it
            c1_index = index 		# and set c1_index to the currently-clicked card's index
            game_state = 1			# move on to next game state (1)

    # Game state 1: if one card is already face-up and a valid choice, on click, do the following: 
    	elif game_state == 1:
        	exposed[index] = True	# unhide it
            c2_index = index        # set c2_index to the currently-clicked card's index
            game_state = 2			# move on to next game state (2)
        
    # Game state 2: if two cards are already face-up, on click, do the followin:
    	else:
        	if deck[c1_index] != deck[c2_index]:  # if the two card values are not the same
              	exposed[c1_index] = False
              	exposed[c2_index] = False

        # assign the current click's choice (index) to c1_index 
        	c1_index = index
    	    exposed[index] = True
        	game_state = 1
        	turn += 1
        	label.set_text("Turns = %s" % str(turn))
        

# cards are logically 50x100 pixels in size 
##
def draw(canvas):
    global deck
    x_coord = 10
    
    for card_index in range(len(deck)):
        if exposed[card_index] == True:
            card_face = str(deck[card_index])
            canvas.draw_text(card_face, (x_coord, 70), 62, 'White')
        else:
            card_corners = [(50 * card_index, 100), (50 * card_index, 0), (50 + 50 * card_index,0), (50 + 50 * card_index, 100)]
            canvas.draw_polygon(card_corners, 2, "Blue", "Green")
        x_coord += 50

        
# create frame and add a button and labels
##
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = %s" % str(turn))

# register event handlers
##
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
##
new_game()
frame.start()


# Always remember to review the grading rubric