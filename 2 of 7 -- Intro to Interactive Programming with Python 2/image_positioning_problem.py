# Image positioning problem

###################################################
# Student should enter code below

import simplegui

# global constants
WIDTH = 400
HEIGHT = 300
img_width = 95
img_height = 93
coords = (WIDTH / 2, HEIGHT / 2)

# load test image (95 x 93 px)
img = simplegui.load_image('http://commondatastorage.googleapis.com/codeskulptor-assets/asteroid.png')

# mouseclick handler
def click(pos):
    global coords
    
    coords = pos
    
# draw handler
def draw(canvas):
    global img, img_width, img_height, coords
    
    canvas.draw_image(img, (img_width / 2, img_height / 2), (img_width, img_height), coords, (img_width, img_height))
    
# create frame and register draw handler    
frame = simplegui.create_frame("Test image", WIDTH, HEIGHT)
frame.set_canvas_background("Gray")
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(click)

# start frame
frame.start()
        
                                       