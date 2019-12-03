#
## Implementation of classic arcade game Pong
##### #####
# Daniel Ashcom
# 1/12/17
###

# cheap imports
###
import simplegui
import random

#
# initialize globals - pos and vel encode vertical info for paddles
##
# constants
WIDTH = 600 # width of canvas
HEIGHT = 400 # height of canvas
BALL_RADIUS = 20 # radius of ball in play
PAD_WIDTH = 8 # width of paddle
PAD_HEIGHT = 80 # height of paddle
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
# hit detection
y1_upper = 0 # track upper edge of player 1's paddle
y1_lower = 0 # track lower edge of player 1's paddle
y2_upper = 0 # track upper edge of player 2's paddle
y2_lower = 0 # track lower edge of player 2's paddle


# Functions
##
def spawn_ball(direction):
    """
    if direction is RIGHT, the ball's velocity is upper right, else upper left
    """
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction == True: # if true, set ball motion toward right
        ball_vel[0] = abs(ball_vel[0])
    else:   # if false, set ball motion toward left
        ball_vel[0] = -ball_vel[0]


def new_game():
    """
    start a new game
    """
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_vel  # numbers
    global score1, score2  # ints
    global RIGHT # boolean representing right-directional play of ball

    # reset the scores
    score1 = 0
    score2 = 0

    # reset paddle positions
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2

    # paddle velocity
    paddle1_vel = 0
    paddle2_vel = 0

    # set random velocity for ball at start of a new game
    rand_x = random.randrange(3, 8)
    rand_y = random.randrange(1, 4)
    
    ball_vel = [rand_x, -rand_y]
    
    # create a new ball with random direction of play
    RIGHT = True
    spawn_ball(RIGHT)
    
    
def draw(canvas):
    """
    handle drawing of playfield, ball, paddles, scores; update ball paddles scores
    """
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, WIDTH, y1_upper, y1_lower, y2_upper, y2_lower # ints
    global  RIGHT # boolean representing right-directional play of ball
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0] # update ball's x position based on its velocity
    ball_pos[1] += ball_vel[1] # update ball's y position based on its velocity
    
    # check for wall collisions and reverse appropriately
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= (HEIGHT - BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
        
    # check for gutter balls and respawn ball with randrange values
    # Gutters are off-set from the edge of the screen by the width of the paddle
    # We also test for the presence of a paddle in order to reflect the ball back
    if ball_pos[0] <= PAD_WIDTH: 
        if ball_pos[1] >= y1_upper and ball_pos[1] <= y1_lower:
            ball_vel[0] = -1.1 * ball_vel[0] # increase difficulty of game by increasing velocity by
            # 10 percent each time the paddle hits the ball
            #
        else: # gutter ball, spawn a new ball toward player 2 and give player 2 a point
            score2 += 1
            RIGHT = True # set direction of spawned ball toward player 2
            spawn_ball(RIGHT)
    elif ball_pos[0] >= WIDTH - PAD_WIDTH:
        if ball_pos[1] >= y2_upper and ball_pos[1] <= y2_lower:
            ball_vel[0] = -1.1 * ball_vel[0]
        else: # gutter ball, spawn a new ball toward player 1 and give player 1 a point
            score1 += 1
            RIGHT = False # set direction of spawned ball toward player 2
            spawn_ball(RIGHT)
    
    # draw ball
    canvas.draw_circle([ball_pos[0], ball_pos[1]], 10, 10, "White", "White")
    
    # Create coordinates for y positions of each of the two vertical coordinates for both player's paddles for the purposes of drawing each paddle
    y1_upper = paddle1_pos - HALF_PAD_HEIGHT # upper y-coordinate of player 1's paddle
    y1_lower = paddle1_pos + HALF_PAD_HEIGHT # lower y-coordinate of player 1's paddle
    y2_upper = paddle2_pos - HALF_PAD_HEIGHT # upper y-coordinate of player 2's paddle
    y2_lower = paddle2_pos + HALF_PAD_HEIGHT # lower y-coordinate of player 2's paddle

    # update paddle's vertical position, keep paddle on the screen
    # paddle1_pos and paddle2_pos define each player's paddle position as the center of each paddle
    # 
    # In order to prevent the paddles from getting stuck at the edge of the screen, 
    # where y1_upper == 0 or y1_lower == HEIGHT, for example, we have to account also
    # for the velocity, thus resolving the sticking problem.
    #
    if y1_upper + paddle1_vel > 0 and y1_lower + paddle1_vel < HEIGHT:
        paddle1_pos += paddle1_vel
        
    if y2_upper + paddle2_vel > 0 and y2_lower + paddle2_vel < HEIGHT:
        paddle2_pos += paddle2_vel
    
    # Draw player 1's paddle
    canvas.draw_polygon([(0, y1_upper), (0, y1_lower), (PAD_WIDTH, y1_lower), (PAD_WIDTH, y1_upper)], 2, "White", "White")
    # Draw player 2's paddle
    canvas.draw_polygon([(WIDTH, y2_upper), (WIDTH, y2_lower), (WIDTH - PAD_WIDTH, y2_lower), (WIDTH - PAD_WIDTH, y2_upper)], 2, "White", "White")
    
    # draw scores
    canvas.draw_text("Player 1: " , (20, 15), 14, "White")
    canvas.draw_text(str(score1), (35, 45), 35, "White")
    canvas.draw_text("Player 2: ", (WIDTH - 70, 15), 14, "White")
    canvas.draw_text(str(score2), (WIDTH - 55, 45), 35, "White")


# Key handlers    
##    
def keydown(key):
    """
    handle key presses for both players, adjusting velocity of paddles accordingly
    """
    global paddle1_vel, paddle2_vel

    # set acceleration of paddle velocity
    accel = 3

    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= accel 
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += accel
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= accel
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += accel
   

def keyup(key):
    """
    handle key releases for both players, setting velocities to zero accordingly
    """
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0


# Button handlers
##
def restart():
    """
    button handler for restarting the game; calls new_game
    """
    new_game()


# Frame
## 
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', restart)

# Start frame
new_game()
frame.start()