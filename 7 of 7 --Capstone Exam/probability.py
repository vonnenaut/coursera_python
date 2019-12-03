# Fundamentals of Computing Capstone Exam
# Question 12
def probability(outcomes):
	""" takes a list of numbers as input (where each number must be between 1 and 6 inclusive) and computes the probability of getting the given sequence of outcomes from rolling the unfair die. Assume the die is rolled exactly the number of times as the length of the outcomes input. """
	total_rolls = len(outcomes)
	individual_probabilities = [0.1, 0.2, 0.3, 0.15, 0.05, 0.2]
	lt_sum = 0 # sum of likelihood of a value times that value times the total number of rolls
	probability = 1

	for idx in range(len(outcomes)-1):
		probability *= individual_probabilities[outcomes[idx]-1]
	return probability

print probability([4, 2, 6, 4, 2, 4, 5, 5, 5, 5, 1, 2, 6, 2, 6, 6, 4, 6, 2, 3, 5, 5, 2, 1, 5, 5, 3, 2, 1, 4, 4, 1, 6, 6, 4, 6, 2, 4, 3, 2, 5, 1, 3, 5, 4, 1, 2, 3, 6, 1])