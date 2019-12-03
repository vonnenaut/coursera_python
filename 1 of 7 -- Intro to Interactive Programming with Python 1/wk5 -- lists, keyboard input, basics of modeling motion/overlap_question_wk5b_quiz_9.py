import simplegui

x = 7
incr = 0

def keydown(key):
    global x
    global incr
    
    incr += 1
    print incr
    x = 2*x - 3

    # if incr in [3, 4, 12]:
    print "After %s press(es), x = %s " % (incr + 1, x)

# def keyup(key):
#    global x

#    x -= 3


frame = simplegui.create_frame('Test', 100, 100)
frame.set_keydown_handler(keydown)
frame.start()