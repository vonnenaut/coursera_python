# Convert the following specification into code. Do the point and  rectangle ever overlap?
# A point starts at [10, 20]. It repeatedly changes position by [3, 0.7] — e.g., under button or timer control. Meanwhile, a rectangle stays in place. Its corners are at [50, 50] (upper left), [180, 50] # (upper right), [180, 140] (lower right), and [50, 140] (lower left).
# To check for overlap, i.e., collision, just run your code and check visually. You do not need to implement a point-rectangle collision test. However, we encourage you to think about how you would implement such a test.
#

import simplegui

# initialize global variables
# canvas
WIDTH = 600
HEIGHT = 400

# a moving point
point_pos = [10, 20]
p_velocity = [3, 0.7]

# a stationary rectangle
rectangle = [[50, 50], [180, 50], [180, 140], [50, 140]]


def draw(canvas):
	point_pos[0] += p_velocity[0]
	point_pos[1] += p_velocity[1]	
	canvas.draw_point(point_pos, 'White')
	canvas.draw_polygon(rectangle, 12, 'Green')
	print point_pos


# define frame, set draw handler and instantiate frame
frame = simplegui.create_frame('Overlap Test', 300, 300)
frame.set_draw_handler(draw)
frame.start()


