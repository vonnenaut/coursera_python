# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global cards, turns, state, exposed   
    turns = 0
    label.set_text("Turns: " + str(turns))
    state = 0
    cards = range(0,8) + range(0,8)
    random.shuffle(cards)
    exposed = [False] * 16
     
# define event handlers
def mouseclick(pos):
    global state, turns, first_card_index, second_card_index    
    clicked_card_index = pos[0] // 50
    if exposed[clicked_card_index] is False: 
        if state == 0:
            exposed[clicked_card_index] = True
            first_card_index = clicked_card_index
            state = 1
        elif state == 1:
            exposed[clicked_card_index] = True
            second_card_index = clicked_card_index
            state = 2
            turns += 1
            label.set_text("Turns: " + str(turns))
        else:
            if cards[first_card_index] != cards[second_card_index]:
                exposed[first_card_index] = False
                exposed[second_card_index] = False
            first_card_index = clicked_card_index
            exposed[clicked_card_index] = True
            state = 1
    
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for card_index in range(len(cards)): 
        card_pos = 50 * card_index
        if exposed[card_index]:
            canvas.draw_text(str(cards[card_index]), [card_pos + 17.5, 60], 30, "white")
        else:
            canvas.draw_line([card_pos + 25, 0], [card_pos + 25, 100], 50, 'green')
            canvas.draw_line([card_pos + 50, 0], [card_pos + 50, 100], 1, 'white')
                
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns:")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()