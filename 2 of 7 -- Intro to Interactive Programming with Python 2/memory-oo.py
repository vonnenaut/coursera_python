# Object-oriented version of Memory card-matching game
# adapted from Coursera project
# by
# Daniel Ashcom

# cheap imports
##
# TO-DO:  import appropriate Kivy modules

# globals
##
CARD_WIDTH = 50
CARD_HEIGHT = 100

# class
##
class Card:
    """ Stores all information related to each card
    """
    # definition of intializer
    def __init__(self, num, exp, loc):
        self.number = num
        self.exposed = exp
        self.location = loc

       
    # definition of getter for number
    def get_number(self):
        return self.number
    
    # check whether card is exposed
    def is_exposed(self):
        return self.exposed
    
    # expose the card
    def expose_card(self):
        self.exposed = True
    
    # hide the card       
    def hide_card(self):
        self.exposed = False
        
    # string method for cards    
    def __str__(self):
        return "Number is " + str(self.number) + ", exposed is " + str(self.exposed)    

    # draw method for cards
    def draw_card(self, canvas):
        if self.exposed is False:
            ## TO-DO:  draw back of card
        elif self.exposed is True:
            ## TO-DO:  draw face of card


    
# draw handler
def draw(canvas):
    card1.draw_card(canvas)
    card2.draw_card(canvas)
    
# create kivy container frame and add a button and labels
## TO-DO:  implement kivy magic

# create cards  
tile1 = Tile(3, True, [0, TILE_HEIGHT])
tile2 = Tile(5, False, [TILE_WIDTH, TILE_HEIGHT])

# start game loop
## TO-DO:  implement kivy magic