# Fundamentals of Computing Capstone Exam
# Question 10
# a simple python stack with the following functions:
# push, which adds an element to the collection, and
# pop, which removes the most recently added element that was not yet removed.
from collections import deque

class Stack():
	""" a simple stack object """
	def __init__(self):
		self.elements = deque()

	def get_stack(self):
		return self.elements

	def Add(self, item):
		""" pushes an item onto the top of the stack """
		print "self.elements:", self.elements
		self.elements.appendleft(item)

	def Rem(self):
		""" pops the most-recently added item from the stack """
		return self.elements.popleft()

st = Stack()
st.Add(4)
st.Add(8)
st.Rem()
st.Add(7)
st.Add(6)
st.Add(5)
st.Rem()
st.Rem()
st.Add(2)
st.Rem()
st.Add(3)
st.Add(7)
print st.get_stack()