# Ball grid slution

###################################################
# Student should enter code below

import simplegui

BALL_RADIUS = 20
GRID_SIZE = 10
WIDTH = 2 * GRID_SIZE * BALL_RADIUS
HEIGHT = 2 * GRID_SIZE * BALL_RADIUS


# define draw
def draw(canvas):
    for x in range(BALL_RADIUS, 400, 2 * BALL_RADIUS):
        for y in range(BALL_RADIUS, 400, 2 * BALL_RADIUS):
            canvas.draw_circle([x, y], BALL_RADIUS, 1, "Blue")
    
# create frame and register handlers
frame = simplegui.create_frame("Ball grid", WIDTH, HEIGHT)
frame.set_draw_handler(draw)

# start frame
frame.start()

