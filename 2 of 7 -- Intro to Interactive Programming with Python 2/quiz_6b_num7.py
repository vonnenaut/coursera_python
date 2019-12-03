"""
Convert the following English description into code.

    Initialize n to be 1000. Initialize numbers to be a
    list of numbers from 2 to n but not including n.
    With results starting as the empty list, repeat the 
    following as long as numbers contains any numbers. 

    Add the first number in numbers to the end of results.
    Remove every number in numbers that is evenly divisible
    by (has no remainder when divided by) the number that 
    you had just added to results.

How long is results?

To test your code, when n is instead 100, the length of results is 25.
"""

n = 1000
results = []

numbers = range(2, n)

while len(numbers) > 0:
    x =numbers[0]
    results.append(x)
    for y in numbers:
        if y % x == 0:
            numbers.remove(y)
       
print len(results)
    
