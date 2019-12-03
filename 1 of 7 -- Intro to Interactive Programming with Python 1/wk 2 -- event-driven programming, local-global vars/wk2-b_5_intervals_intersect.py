# Coursera Fundamentals of Computing (7-part series)
# Pt 1: An Introduction to Interactive Programming in Python (Pt 1)
# wk 2-b
# # 5 test if two intervals intersect
###################################################
# Interval intersection formula
# Student should enter function on the next lines.
#
# Write a Python function interval_intersect that 
#takes parameters a, b, c, and d and returns True 
#if the intervals [a,b] and [c,d] intersect and 
# False otherwise. While this test may seem tricky,
# the solution is actually very simple and consists 
# of one line of Python code. (You may assume that a≤b
# and c≤d.)

def interval_intersect(a, b, c, d):
    if a > d or c > b:
        return False
    else:
        return True