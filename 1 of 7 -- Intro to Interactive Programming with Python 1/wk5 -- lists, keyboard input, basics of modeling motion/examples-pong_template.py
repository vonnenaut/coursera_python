# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600 # width of canvas
HEIGHT = 400 # height of canvas
BALL_RADIUS = 20 # radius of ball in play
PAD_WIDTH = 8 # width of paddle
PAD_HEIGHT = 80 # height of paddle
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False # set inital ball direction of play
RIGHT = True #   toward player 2
score1 = 0 # set initial score
score2 = 0 #
ball_pos = [0, 0] # initialize ball_pos and ball_vel for new ball in middle of table
ball_vel = [0, 0] # instantiate velocity with zero x-y values

# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    rand_x = random.randrange(3, 8)
    rand_y = random.randrange(1, 4)
    
    if direction == True: # ball is headed toward the right
        ball_vel = [rand_x, -rand_y]
    else: # ball is headed toward the left
        ball_vel = [-rand_x, -rand_y]
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    global RIGHT # boolean representing right-directional play of ball
    
    spawn_ball(RIGHT) # spawn the game ball passing the boolean for right-directional motion

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, WIDTH
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0] # update ball's x position based on its velocity
    ball_pos[1] += ball_vel[1] # update ball's y position based on its velocity
    
    # check for wall collisions and reverse appropriately
    if ball_pos[1] <= (BALL_RADIUS) or ball_pos[1] >= (HEIGHT - BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
        
    # check for gutter balls and respawn ball with randrange values
    if ball_pos[0] <= 0 or ball_pos[0] >= WIDTH:
        dir = random.randrange(0, 2)
        if dir == 0:
            dir = True # right-directional ball play
        else:
            dir = False # left-directional ball play
        print dir
        spawn_ball(dir)
    
    # draw ball
    canvas.draw_circle([ball_pos[0], ball_pos[1]], 10, 10, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    
    # draw paddles
    canvas.draw_polygon([(10, 30), (10, 30 + PAD_HEIGHT), (10 + PAD_WIDTH, 30), (10 + PAD_WIDTH, 30 + PAD_HEIGHT)], 10, "White")
    canvas.draw_polygon([(WIDTH - 10, 30), (WIDTH - 10, 30 + PAD_HEIGHT), (WIDTH - (10 + PAD_WIDTH), 30 + PAD_HEIGHT), (WIDTH - (10 + PAD_WIDTH), 30)], 10, "White")
    
    # determine whether paddle and ball collide    
    
    # draw scores
    canvas.draw_text("Player 1\n" + str(score1), (20, 25), 30, "White")
    canvas.draw_text("Player 2\n" + str(score2), (WIDTH - 35, 25), 30, "White")
                     
def keydown(key):
    global paddle1_vel, paddle2_vel
   
def keyup(key):
    global paddle1_vel, paddle2_vel


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
